<template>
    <div>
        <el-button @click="startAnimation">
            <el-icon>
                <svg t="1726291468217" class="icon" viewBox="0 0 1024 1024" version="1.1"
                    xmlns="http://www.w3.org/2000/svg" p-id="1478" width="200" height="200">
                    <path
                        d="M675.328 117.717333A425.429333 425.429333 0 0 0 512 85.333333C276.352 85.333333 85.333333 276.352 85.333333 512s191.018667 426.666667 426.666667 426.666667 426.666667-191.018667 426.666667-426.666667c0-56.746667-11.093333-112-32.384-163.328a21.333333 21.333333 0 0 0-39.402667 16.341333A382.762667 382.762667 0 0 1 896 512c0 212.074667-171.925333 384-384 384S128 724.074667 128 512 299.925333 128 512 128c51.114667 0 100.8 9.984 146.986667 29.12a21.333333 21.333333 0 0 0 16.341333-39.402667zM456.704 305.92C432.704 289.152 405.333333 303.082667 405.333333 331.797333v360.533334c0 28.586667 27.541333 42.538667 51.370667 25.856l252.352-176.768c21.76-15.253333 21.632-43.541333 0-58.709334l-252.373333-176.768z m-8.597333 366.72V351.466667l229.269333 160.597333-229.269333 160.597333z"
                        fill="#3D3D3D" p-id="1479"></path>
                </svg>
            </el-icon>
        </el-button>
        <div ref="container" style="width: 800px; height: 600px;"></div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { ElButton } from 'element-plus';
import 'element-plus/dist/index.css';

const container = ref(null);
let scene, camera, renderer, controls;
let inputGroup, kernelGroup, resultGroup;
let steps = [];
let stepIndex = 0;
const cubeSize = 1; // 小立方体的尺寸
const gap = 0.3; // 小立方体之间的间隔
const inputSize = 4; // 输入数据的尺寸
const kernelSize = 3; // 卷积核的尺寸

const initScene = () => {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, 800 / 600, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(800, 600);
    container.value.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // 创建输入数据
    inputGroup = new THREE.Group();
    const inputData = [];
    for (let x = 0; x < inputSize; x++) {
        inputData[x] = [];
        for (let y = 0; y < inputSize; y++) {
            inputData[x][y] = [];
            for (let z = 0; z < inputSize; z++) {
                const value = Math.floor(Math.random() * 10);
                inputData[x][y][z] = value;
                const geometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
                const material = new THREE.MeshBasicMaterial({ color: 0x87CEEB, transparent: true,opacity : 0.5 });
                const cube = new THREE.Mesh(geometry, material);
                cube.position.set(
                    x * (cubeSize + gap),
                    y * (cubeSize + gap),
                    z * (cubeSize + gap)
                );
                inputGroup.add(cube);
            }
        }
    }
    scene.add(inputGroup);

    // 创建卷积核
    kernelGroup = new THREE.Group();
    const kernelData = [];
    for (let x = 0; x < kernelSize; x++) {
        kernelData[x] = [];
        for (let y = 0; y < kernelSize; y++) {
            kernelData[x][y] = [];
            for (let z = 0; z < kernelSize; z++) {
                const value = Math.floor(Math.random() * 3) - 1; // 卷积核值在[-1, 1]之间
                kernelData[x][y][z] = value;
                const geometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
                const material = new THREE.MeshBasicMaterial({ color: 0xFFA07A, transparent: false });
                const cube = new THREE.Mesh(geometry, material);
                cube.position.set(
                    x * (cubeSize + gap),
                    y * (cubeSize + gap),
                    z * (cubeSize + gap)
                );
                kernelGroup.add(cube);
            }
        }
    }
    scene.add(kernelGroup);

    // 创建卷积结果组
    resultGroup = new THREE.Group();
    scene.add(resultGroup);

    // 让立方体倾斜
    inputGroup.rotation.x = Math.PI / 4;
    inputGroup.rotation.y = Math.PI / 4;
    kernelGroup.rotation.x = Math.PI / 4;
    kernelGroup.rotation.y = Math.PI / 4;
    resultGroup.rotation.x = Math.PI / 4;
    resultGroup.rotation.y = Math.PI / 4;

    camera.position.set(10, 10, 20);
    camera.lookAt(scene.position);

    // 实现卷积计算并展示每一步的结果
    const convolve3D = (inputData: number[][][], kernelData: number[][][]) => {
        const outputSize = inputData.length - kernelData.length + 1;
        const outputData = [];
        for (let x = 0; x < outputSize; x++) {
            outputData[x] = [];
            for (let y = 0; y < outputSize; y++) {
                outputData[x][y] = [];
                for (let z = 0; z < outputSize; z++) {
                    let sum = 0;
                    for (let i = 0; i < kernelData.length; i++) {
                        for (let j = 0; j < kernelData.length; j++) {
                            for (let k = 0; k < kernelData.length; k++) {
                                sum += inputData[x + i][y + j][z + k] * kernelData[i][j][k];
                            }
                        }
                    }
                    outputData[x][y][z] = sum;
                }
            }
        }
        return outputData;
    };

    const outputData = convolve3D(inputData, kernelData);
    steps = [];
    for (let x = 0; x < outputData.length; x++) {
        for (let y = 0; y < outputData.length; y++) {
            for (let z = 0; z < outputData.length; z++) {
                steps.push({ x, y, z, value: outputData[x][y][z] });
            }
        }
    }
};

const showStep = () => {
    if (stepIndex < steps.length) {
        const { x, y, z, value } = steps[stepIndex];
        kernelGroup.position.set(
            x * (cubeSize + gap),
            y * (cubeSize + gap),
            z * (cubeSize + gap)
        );

        // 在卷积核移动到新位置后，显示卷积结果
        const geometry = new THREE.BoxGeometry(cubeSize, cubeSize, cubeSize);
        const material = new THREE.MeshBasicMaterial({ color: 0x32CD32, transparent: false });
        const resultCube = new THREE.Mesh(geometry, material);
        resultCube.position.set(
            x * (cubeSize + gap) + 10, // 将结果立方体放置在输入数据旁边
            y * (cubeSize + gap),
            z * (cubeSize + gap)
        );
        resultGroup.add(resultCube);

        stepIndex++;
        setTimeout(showStep, 1000); // 每一步暂停1秒
    }
};

const animate = () => {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
};

const startAnimation = () => {
    // 清空结果组
    while (resultGroup.children.length) {
        resultGroup.remove(resultGroup.children[0]);
    }
    stepIndex = 0;
    showStep();
};

onMounted(() => {
    initScene();
    animate();
});
</script>

<style scoped>
div {
    border: 1px solid black;
}
</style>