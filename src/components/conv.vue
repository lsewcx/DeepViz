<template>
    <div ref="convContainer" class="conv-container"></div>
    <div ref="formulaContainer" class="formula-container"></div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import * as d3 from 'd3';


const convContainer = ref(null);
const formulaContainer = ref(null);

onMounted(() => {
    const data: Array = [
        [1, 2, 4, 6,7,8],
        [4, 5, 6, 7,9,8],
        [7, 8, 9, 8,9,6]
    ];

    const kernel: Array = [
        [1, 1]
    ];

    const cellSize: Number = 50;
    const padding: Number = 5;

    const dataHeight = data.length;
    const dataWidth = data[0].length;
    const kernelHeight = kernel.length;
    const kernelWidth = kernel[0].length;

    const resultHeight = dataHeight - kernelHeight + 1;
    const resultWidth = dataWidth - kernelWidth + 1;
    //自动根据输入的数组大小和卷积核的大小计算结果矩阵的大小
    const result = Array.from({ length: resultHeight }, () => Array(resultWidth).fill(0));

    // 计算 SVG 容器的宽度和高度
    const svgWidth: Number = (data[0].length + kernel[0].length + result[0].length + 2) * (cellSize + padding);
    const svgHeight: Number = Math.max(data.length, kernel.length, result.length) * (cellSize + padding) + padding;

    // Create SVG element
    const container = d3.select(convContainer.value);
    //这个是画布的问题
    const svg = container.append('svg')
        .attr('width', '100%')
        .attr('height', '60%')
        .attr('viewBox', `0 0 ${svgWidth} ${svgHeight}`)
        .attr('preserveAspectRatio', 'xMidYMid meet');

    // Draw input matrix
    const inputGroup = svg.append('g')
        .attr('transform', `translate(${padding}, ${padding})`);

    inputGroup.selectAll('rect')
        .data(data.flat())
        .enter()
        .append('rect')
        .attr('x', (d, i) => (i % data[0].length) * (cellSize + padding))
        .attr('y', (d, i) => Math.floor(i / data[0].length) * (cellSize + padding))
        .attr('width', cellSize)
        .attr('height', cellSize)
        .attr('fill', 'lightblue')
        .attr('stroke', 'black');

    inputGroup.selectAll('text')
        .data(data.flat())
        .enter()
        .append('text')
        .attr('x', (d, i) => (i % data[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('y', (d, i) => Math.floor(i / data[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .text(d => d);

    // Draw kernel matrix
    const kernelGroup = svg.append('g')
        .attr('transform', `translate(${(data[0].length + 1) * (cellSize + padding)}, ${padding})`);

    kernelGroup.selectAll('rect')
        .data(kernel.flat())
        .enter()
        .append('rect')
        .attr('x', (d, i) => (i % kernel[0].length) * (cellSize + padding))
        .attr('y', (d, i) => Math.floor(i / kernel[0].length) * (cellSize + padding))
        .attr('width', cellSize)
        .attr('height', cellSize)
        .attr('fill', 'lightgreen')
        .attr('stroke', 'black');

    kernelGroup.selectAll('text')
        .data(kernel.flat())
        .enter()
        .append('text')
        .attr('x', (d, i) => (i % kernel[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('y', (d, i) => Math.floor(i / kernel[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .text(d => d);

    // Draw result matrix
    const resultGroup = svg.append('g')
        .attr('transform', `translate(${(data[0].length + kernel[0].length + 2) * (cellSize + padding)}, ${padding})`);

    resultGroup.selectAll('rect')
        .data(result.flat())
        .enter()
        .append('rect')
        .attr('x', (d, i) => (i % result[0].length) * (cellSize + padding))
        .attr('y', (d, i) => Math.floor(i / result[0].length) * (cellSize + padding))
        .attr('width', cellSize)
        .attr('height', cellSize)
        .attr('fill', 'lightcoral')
        .attr('stroke', 'black');

    const resultText = resultGroup.selectAll('text')
        .data(result.flat())
        .enter()
        .append('text')
        .attr('x', (d, i) => (i % result[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('y', (d, i) => Math.floor(i / result[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .text(d => d);

    // Animate convolution operation
    const animateConvolution = async () => {
        for (let i = 0; i < data.length - kernel.length + 1; i++) {
            for (let j = 0; j < data[0].length - kernel[0].length + 1; j++) {
                let sum = 0;
                let formula = '';
                for (let ki = 0; ki < kernel.length; ki++) {
                    for (let kj = 0; kj < kernel[0].length; kj++) {
                        const dataValue = data[i + ki][j + kj];
                        const kernelValue = kernel[ki][kj];
                        sum += dataValue * kernelValue;
                        formula += `${dataValue} * ${kernelValue} + `;
                    }
                }
                formula = formula.slice(0, -3); // Remove the last ' + '
                result[i][j] = sum;

                // Update formula display
                d3.select(formulaContainer.value).text(`公式: ${formula} = ${sum}`);

                // Update result matrix
                resultText.data(result.flat())
                    .text(d => d);

                // Highlight current convolution area
                inputGroup.selectAll('rect')
                    .attr('fill', (d, index) => {
                        const x = index % data[0].length;
                        const y = Math.floor(index / data[0].length);
                        if (x >= j && x < j + kernel[0].length && y >= i && y < i + kernel.length) {
                            return 'orange';
                        }
                        return 'lightblue';
                    });

                // Wait for a short duration before moving to the next step
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
    };

    animateConvolution();
});
</script>

<style scoped>
.conv-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    /* 减少顶部间距 */
    width: 100%;
    height: 60vh;
    /* 减少高度 */
    transform: scale(0.8);
    /* 缩小比例 */
    transform-origin: top;
    /* 设置缩放原点 */
}

.formula-container {
    text-align: center;
    margin-top: 1px;
    /* 减少顶部间距 */
    font-size: 18px;
    /* 减小字体大小 */
    font-weight: bold;

    transform: scale(1);
    /* 缩小比例 */
    transform-origin: top;
    /* 设置缩放原点 */
}
</style>