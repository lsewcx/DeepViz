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
    const data = [
        [1, 2, 4, 6],
        [4, 5, 6, 7],
        [7, 8, 9, 8]
    ];
    
    const kernel = [
        [1, 1]
    ];

    const cellSize = 50;
    const padding = 5;
    const paddingZeros = 1; // 填充0的数量
    const step = 3; // 步长

    // 在数据矩阵周围添加填充0
    const paddedData = Array.from({ length: data.length + 2 * paddingZeros }, (_, i) => 
        Array.from({ length: data[0].length + 2 * paddingZeros }, (_, j) => 
            (i >= paddingZeros && i < data.length + paddingZeros && j >= paddingZeros && j < data[0].length + paddingZeros) 
                ? data[i - paddingZeros][j - paddingZeros] 
                : 0
        )
    );

    const dataHeight = paddedData.length;
    const dataWidth = paddedData[0].length;
    const kernelHeight = kernel.length;
    const kernelWidth = kernel[0].length;

    const resultHeight = Math.floor((dataHeight - kernelHeight) / step) + 1;
    const resultWidth = Math.floor((dataWidth - kernelWidth) / step) + 1;

    const result = Array.from({ length: resultHeight }, () => Array(resultWidth).fill(0));

    const svgWidth = (paddedData[0].length + kernel[0].length + result[0].length + 2) * (cellSize + padding);
    const svgHeight = Math.max(paddedData.length, kernel.length, result.length) * (cellSize + padding) + padding;

    const container = d3.select(convContainer.value);
    const svg = container.append('svg')
        .attr('width', svgWidth)
        .attr('height', svgHeight)
        .attr('viewBox', `0 0 ${svgWidth} ${svgHeight}`)
        .attr('preserveAspectRatio', 'xMidYMin meet'); // 修改为 xMidYMin 以减少顶部空白

    const inputGroup = svg.append('g')
        .attr('transform', `translate(${padding}, ${padding})`);

    inputGroup.selectAll('rect')
        .data(paddedData.flat())
        .enter()
        .append('rect')
        .attr('x', (d, i) => (i % paddedData[0].length) * (cellSize + padding))
        .attr('y', (d, i) => Math.floor(i / paddedData[0].length) * (cellSize + padding))
        .attr('width', cellSize)
        .attr('height', cellSize)
        .attr('fill', 'lightblue')
        .attr('stroke', 'black');

    inputGroup.selectAll('text')
        .data(paddedData.flat())
        .enter()
        .append('text')
        .attr('x', (d, i) => (i % paddedData[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('y', (d, i) => Math.floor(i / paddedData[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .text(d => d);

    const kernelGroup = svg.append('g')
        .attr('transform', `translate(${(paddedData[0].length + 1) * (cellSize + padding)}, ${padding})`);

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

    const resultGroup = svg.append('g')
        .attr('transform', `translate(${(paddedData[0].length + kernel[0].length + 2) * (cellSize + padding)}, ${padding})`);

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

    const animateConvolution = async () => {
        for (let i = 0; i <= dataHeight - kernelHeight; i += step) {
            for (let j = 0; j <= dataWidth - kernelWidth; j += step) {
                let sum = 0;
                let formula = '';
                for (let ki = 0; ki < kernel.length; ki++) {
                    for (let kj = 0; kj < kernel[0].length; kj++) {
                        const dataValue = paddedData[i + ki][j + kj];
                        const kernelValue = kernel[ki][kj];
                        sum += dataValue * kernelValue;
                        formula += `${dataValue} * ${kernelValue} + `;
                    }
                }
                formula = formula.slice(0, -3);
                result[Math.floor(i / step)][Math.floor(j / step)] = sum;

                d3.select(formulaContainer.value).text(`公式: ${formula} = ${sum}`);

                resultText.data(result.flat())
                    .text(d => d);

                inputGroup.selectAll('rect')
                    .attr('fill', (d, index) => {
                        const x = index % paddedData[0].length;
                        const y = Math.floor(index / paddedData[0].length);
                        if (x >= j && x < j + kernel[0].length && y >= i && y < i + kernel.length) {
                            return 'orange';
                        }
                        return 'lightblue';
                    });

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
    width: 100%;
    height: 80vh; /* 调整高度以适应新的结果矩阵 */
    overflow: auto; /* 允许滚动以防止内容被遮挡 */
}

.formula-container {
    text-align: center;
    margin-top: 5px; /* 减少上边距 */
    font-size: 18px;
    font-weight: bold;
}
</style>