import json
import os
from loguru import logger
from matplotlib import pyplot as plt
import torch
import netron.source
from utils.folder import check_path_exists
import matplotlib
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from model import TinyVGG
import inspect
from PIL import Image
from compute import *

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
                if isinstance(param_value, str) and 'Parameter containing:' in param_value:
                    param_value = param_value.replace('Parameter containing:\n', '').strip()
                layer_params[param_name] = param_value
        return layer_params

    @staticmethod
    def print_model_layers(model: torch.nn.Module) -> None:
        model_structure = {}
        for name, layer in model.named_children():
            layer_params = ModelInspector.get_layer_parameters(layer)
            model_structure[name] = {
                'type': type(layer).__name__,
                'parameters': layer_params
            }
        
        # 将模型结构保存到 JSON 文件中
        with open('model_structure.json', 'w') as f:
            json.dump(model_structure, f, indent=4)
        logger.info(f'Model structure saved to model_structure.json')

class ModelVisualizer:
    @staticmethod
    def get_output_and_plot(model, image: str, output_dir='img') -> None:
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
        for name, output in activation.items():
            output = output.detach().numpy()
            if output.ndim == 4:
                output = output[:, 0, :, :]
            for j in range(output.shape[0]):
                if output.ndim == 2:  # 如果是全连接层的输出，跳过
                    continue
                plt.imshow(output[j], cmap='gray')
                plt.savefig(os.path.join(output_dir, f'output_layer_{name}_sample_{j+1}.png'))
                plt.close()
        logger.info(f'Output images saved to {output_dir}')

class JsonHandler:
    @staticmethod
    def read_json(path: str) -> dict:
        with open(path, 'r') as f:
            data = json.load(f)
        logger.info(data.keys())
        return data

def vis() -> None:
    image = ImageProcessor.preprocess_image('0-label-5.png')
    model = ModelLoader.load_model('tinyvgg_model.pth')
    ModelInspector.print_model_layers(model)
    ModelVisualizer.get_output_and_plot(model, image)
    
if __name__ == '__main__':
    vis()