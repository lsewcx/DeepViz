<template>
    <a-image :width="200" src="https://p1-arco.byteimg.com/tos-cn-i-uwbnlip3yd/a8c8cdb109cb051163646151a4a5083b.png~tplv-uwbnlip3yd-webp.webp" />
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { loadModel } from '../utils/onnx';

onMounted(async () => {
    await loadModel('/model/cifar_net.onnx');
    // 在这里添加其他需要在模型加载完毕后执行的代码
});
</script>