import json
import os
from loguru import logger
from matplotlib import pyplot as plt
import torch
from utils.folder import check_path_exists
import matplotlib
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import TinyVGG
import inspect
from PIL import Image
from rich import print

# 使用相对导入
from netron.source.server import *

try:
    matplotlib.use('TkAgg')
except Exception as e:
    print(f"Error setting matplotlib backend: {e}")

class ImageProcessor:
    @staticmethod
    def preprocess_image(image_path: str) -> torch.Tensor:
        transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        image = Image.open(image_path)
        image = transform(image).unsqueeze(0)  # 添加批次维度
        return image

class ModelLoader:
    @staticmethod
    def load_model(model_path: str) -> torch.nn.Module:
        try:
            model = torch.load(model_path)
        except Exception as e:
            logger.error(f'Error loading model: {e}')
            return None
        model.eval()
        return model

class ModelInspector:
    @staticmethod
    def get_layer_parameters(layer) -> dict:
        # 获取层的所有参数
        params = inspect.signature(layer.__init__).parameters
        layer_params = {}
        for param_name, param in params.items():
            if param_name != 'self':  # 跳过 'self' 参数
                param_value = getattr(layer, param_name, 'N/A')
                if isinstance(param_value, torch.nn.Parameter):
                    param_value = param_value.detach().cpu().numpy().tolist()  # 转换为列表以便序列化为 JSON
                elif isinstance(param_value, (torch.Tensor, torch.nn.Module)):
                    param_value = str(param_value)
                elif isinstance(param_value, (list, tuple)):
                    param_value = [str(v) if isinstance(v, torch.nn.Module) else v for v in param_value]
                if isinstance(param_value, str) and 'Parameter containing:' in param_value:
                    param_value = param_value.replace('Parameter containing:\n', '').strip()
                layer_params[param_name] = param_value
        return layer_params

    @staticmethod
    def get_model_structure(model: torch.nn.Module, parent_name: str = '', connect_to: str = None) -> dict:
        model_structure = {}
        children = list(model.named_children())
        for i, (name, layer) in enumerate(children):
            full_name = f"{parent_name}.{name}" if parent_name else name
            layer_params = ModelInspector.get_layer_parameters(layer)
            next_layer_name = children[i + 1][0] if i + 1 < len(children) else None
            submodules = ModelInspector.get_model_structure(layer, full_name, next_layer_name) if len(list(layer.named_children())) > 0 else None
            model_structure[full_name] = {
                'type': type(layer).__name__,
                'parameters': layer_params,
                'connect_to': next_layer_name,
                'submodules': submodules
            }
        return model_structure

    @staticmethod
    def save_model_structure(model: torch.nn.Module, file_path: str) -> None:
        model_structure = ModelInspector.get_model_structure(model)
        
        # 将模型结构保存到 JSON 文件中
        with open(file_path, 'w') as f:
            json.dump(model_structure, f, indent=4, default=str)
        logger.info(f'Model structure saved to {file_path}')

class ModelVisualizer:
    @staticmethod
    def get_output_and_plot(model, image: torch.Tensor, output_dir='img') -> dict:
        check_path_exists(output_dir)
        weights = {}
        activation = {}

        def get_activation(name):
            def hook(model, input, output):
                activation[name] = output.detach()
            return hook

        for name, layer in model.named_children():
            layer.register_forward_hook(get_activation(name))

        image = image.to('cpu')
        output = model(image)

        for name, param in model.named_parameters():
            weights[name] = param.detach().cpu().numpy().tolist()  # 转换为列表以便序列化为 JSON

        # 将权重保存为 JSON 文件
        with open('model_weights.json', 'w') as f:
            json.dump(weights, f)
        logger.info(f'Model weights saved to {output_dir}')
        
        # 保存原始输入图像
        output_images = {}
        for name, output in activation.items():
            output = output.detach().numpy()
            if output.ndim == 4:
                output = output[:, 0, :, :]
            for j in range(output.shape[0]):
                if output.ndim == 2:  # 如果是全连接层的输出，跳过
                    continue
                image_path = os.path.join(output_dir, f'output_layer_{name}_sample_{j+1}.png')
                plt.imshow(output[j], cmap='gray')
                plt.savefig(image_path)
                plt.close()
                output_images[f'{name}_sample_{j+1}'] = image_path
        logger.info(f'Output images saved to {output_dir}')
        
        return {
            'weights': weights,
            'output_images': output_images
        }

class JsonHandler:
    @staticmethod
    def read_json(path: str) -> dict:
        with open(path, 'r') as f:
            data = json.load(f)
        logger.info(data.keys())
        return data

def vis() -> None:
    image = ImageProcessor.preprocess_image('0-label-5.png')
    model = ModelLoader.load_model('modelcpu.pth')
    if model is not None:
        model_structure_path = 'model_structure.json'
        ModelInspector.save_model_structure(model, model_structure_path)
        
        output_data = ModelVisualizer.get_output_and_plot(model, image)
        
        # 将模型结构和输出数据合并保存到一个 JSON 文件中
        with open('model_full_structure.json', 'w') as f:
            json.dump({
                'model_structure': JsonHandler.read_json(model_structure_path),
                'output_data': output_data
            }, f, indent=4)
        logger.info(f'Full model structure and output data saved to model_full_structure.json')

def netron_json() -> None:
    # get_json('vis/tinyvgg_model.pth')
    serve('vis/tinyvgg_model.pth')
    # get_json('vis/tinyvgg_model.pth')


if __name__ == '__main__':
    netron_json()