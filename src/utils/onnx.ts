import * as ort from 'onnxruntime-web';

const env = ort.env;
ort.env.debug = true;
env.logLevel = 'info';
//https://onnxruntime.ai/docs/tutorials/web/env-flags-and-session-options.html 这里的代码查看这个文档
env.wasm.wasmPaths = 'https://cdn.jsdelivr.net/npm/onnxruntime-web@1.19.2/dist/';

// 读取 ONNX 模型
export async function loadModel(modelUrl: string) {
  try {
    console.log('Starting to load model from URL:', modelUrl);
    const startTime = performance.now();

    // 创建 InferenceSession，指定后端为 CPU
    const session = await ort.InferenceSession.create(modelUrl, { executionProviders: ['cpu'] });
    const endTime = performance.now();
    console.log(`InferenceSession created successfully in ${(endTime - startTime).toFixed(2)} ms`);


  } catch (error) {
    console.error('Failed to load the model:', error);
  }
}