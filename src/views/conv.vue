<template>
    <div class="slider-demo-block">
        <span class="demonstration">padding</span>
        <el-slider v-model="paddingZeros" :min="0" :max="3" @input="updateConvolution" class="small-slider" />
    </div>
    <div class="slider-demo-block">
        <span class="demonstration">step</span>
        <el-slider v-model="step" :min="1" :max="3" @input="updateConvolution" class="small-slider" />
    </div>
    <el-button @click="startAnimation">
        <el-icon>
            <svg t="1726291468217" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                p-id="1478" width="200" height="200">
                <path
                    d="M675.328 117.717333A425.429333 425.429333 0 0 0 512 85.333333C276.352 85.333333 85.333333 276.352 85.333333 512s191.018667 426.666667 426.666667 426.666667 426.666667-191.018667 426.666667-426.666667c0-56.746667-11.093333-112-32.384-163.328a21.333333 21.333333 0 0 0-39.402667 16.341333A382.762667 382.762667 0 0 1 896 512c0 212.074667-171.925333 384-384 384S128 724.074667 128 512 299.925333 128 512 128c51.114667 0 100.8 9.984 146.986667 29.12a21.333333 21.333333 0 0 0 16.341333-39.402667zM456.704 305.92C432.704 289.152 405.333333 303.082667 405.333333 331.797333v360.533334c0 28.586667 27.541333 42.538667 51.370667 25.856l252.352-176.768c21.76-15.253333 21.632-43.541333 0-58.709334l-252.373333-176.768z m-8.597333 366.72V351.466667l229.269333 160.597333-229.269333 160.597333z"
                    fill="#3D3D3D" p-id="1479"></path>
            </svg>
        </el-icon>
    </el-button>
    <div ref="convContainer" class="conv-container"></div>
    <div ref="formulaContainer" class="formula-container"></div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import * as d3 from 'd3';

const convContainer = ref(null);
const formulaContainer = ref(null);
const paddingZeros = ref(1); // 默认填充0的数量
const step = ref(1); // 默认步长

const data = ref([
    [1, 2, 4, 6],
    [4, 5, 6, 7],
    [7, 8, 9, 8]
]);

const kernel = ref([
    [1, 1],
    [1, 2]
]);

const cellSize = 50;
const padding = 5;


const updateValue = (type, row, col, value) => {
    const newValue = parseFloat(prompt(`请输入新的值 (当前值: ${value})`, value));
    if (!isNaN(newValue)) {
        if (type === 'data') {
            data.value[row][col] = newValue;
        } else if (type === 'kernel') {
            kernel.value[row][col] = newValue;
        }
        updateConvolution();
    }
};

const updateConvolution = () => {
    if (!convContainer.value) return;

    // 清空之前的内容
    d3.select(convContainer.value).selectAll('*').remove();

    // 在数据矩阵周围添加填充0
    const paddedData = Array.from({ length: data.value.length + 2 * paddingZeros.value }, (_, i) =>
        Array.from({ length: data.value[0].length + 2 * paddingZeros.value }, (_, j) =>
            (i >= paddingZeros.value && i < data.value.length + paddingZeros.value && j >= paddingZeros.value && j < data.value[0].length + paddingZeros.value)
                ? data.value[i - paddingZeros.value][j - paddingZeros.value]
                : 0
        )
    );

    const dataHeight = paddedData.length;
    const dataWidth = paddedData[0].length;
    const kernelHeight = kernel.value.length;
    const kernelWidth = kernel.value[0].length;

    const resultHeight = Math.floor((dataHeight - kernelHeight) / step.value) + 1;
    const resultWidth = Math.floor((dataWidth - kernelWidth) / step.value) + 1;

    const result = Array.from({ length: resultHeight }, () => Array(resultWidth).fill(0));

    const svgWidth = (paddedData[0].length + kernel.value[0].length + result[0].length + 2) * (cellSize + padding);
    const svgHeight = Math.max(paddedData.length, kernel.value.length, result.length) * (cellSize + padding) + padding;

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
        .attr('stroke', 'black')
        .attr('data-index', (d, i) => i);

    inputGroup.selectAll('text')
        .data(paddedData.flat())
        .enter()
        .append('text')
        .attr('x', (d, i) => (i % paddedData[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('y', (d, i) => Math.floor(i / paddedData[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .text(d => d)
        .on('click', function (event, d) {
            const index = paddedData.flat().indexOf(d);
            const row = Math.floor(index / paddedData[0].length);
            const col = index % paddedData[0].length;
            updateValue('data', row - paddingZeros.value, col - paddingZeros.value, d);
        });

    const kernelGroup = svg.append('g')
        .attr('transform', `translate(${(paddedData[0].length + 1) * (cellSize + padding)}, ${padding})`);

    kernelGroup.selectAll('rect')
        .data(kernel.value.flat())
        .enter()
        .append('rect')
        .attr('x', (d, i) => (i % kernel.value[0].length) * (cellSize + padding))
        .attr('y', (d, i) => Math.floor(i / kernel.value[0].length) * (cellSize + padding))
        .attr('width', cellSize)
        .attr('height', cellSize)
        .attr('fill', 'lightgreen')
        .attr('stroke', 'black');

    kernelGroup.selectAll('text')
        .data(kernel.value.flat())
        .enter()
        .append('text')
        .attr('x', (d, i) => (i % kernel.value[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('y', (d, i) => Math.floor(i / kernel.value[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .text(d => d)
        .on('click', function (event, d) {
            const index = kernel.value.flat().indexOf(d);
            const row = Math.floor(index / kernel.value[0].length);
            const col = index % kernel.value[0].length;
            updateValue('kernel', row, col, d);
        });

    const resultGroup = svg.append('g')
        .attr('transform', `translate(${(paddedData[0].length + kernel.value[0].length + 2) * (cellSize + padding)}, ${padding})`);

    resultGroup.selectAll('rect')
        .data(result.flat().map((d, i) => ({ value: d, index: i })))
        .enter()
        .append('rect')
        .attr('x', (d, i) => (i % result[0].length) * (cellSize + padding))
        .attr('y', (d, i) => Math.floor(i / result[0].length) * (cellSize + padding))
        .attr('width', cellSize)
        .attr('height', cellSize)
        .attr('fill', 'lightcoral')
        .attr('stroke', 'black')
        .on('click', function (event, d) {
            // 计算点击的块在结果矩阵中的位置
            const resultX = d.index % result[0].length;
            const resultY = Math.floor(d.index / result[0].length);

            // 清空之前高亮显示的输入矩阵和卷积核
            inputGroup.selectAll('rect').attr('fill', 'lightblue');
            kernelGroup.selectAll('rect').attr('fill', 'lightgreen');

            // 计算点击的块在输入矩阵中的对应位置
            const inputStartX = resultX * step.value;
            const inputStartY = resultY * step.value;
            // 计算输入矩阵中需要高亮显示的区域
            for (let i = 0; i < kernelHeight; i++) {
                for (let j = 0; j < kernelWidth; j++) {
                    const inputIndex = (inputStartY + i) * paddedData[0].length + (inputStartX + j);
                    inputGroup.select('rect[data-index="' + inputIndex + '"]').attr('fill', 'orange');
                }
            }

            // 计算并高亮显示卷积核中对应的元素
            for (let i = 0; i < kernelHeight; i++) {
                for (let j = 0; j < kernelWidth; j++) {
                    const kernelIndex = i * kernelWidth + j;
                    kernelGroup.select('rect[data-index="' + kernelIndex + '"]').attr('fill', 'orange');
                }
            }

            // 显示公式
            let formula = '';
            for (let i = 0; i < kernelHeight; i++) {
                for (let j = 0; j < kernelWidth; j++) {
                    const inputValue = paddedData[inputStartY + i][inputStartX + j];
                    const kernelValue = kernel.value[i][j];
                    formula += `${inputValue} * ${kernelValue} + `;
                }
            }
            formula = formula.slice(0, -3); // Remove the last ' + '
            d3.select(formulaContainer.value).text(`公式: ${formula} = ${d.value}`);

            // 重置被点击的卷积结果块的颜色
            resultGroup.selectAll('rect').attr('fill', (di, i) => {
                const blockX = i % result[0].length;
                const blockY = Math.floor(i / result[0].length);
                return (blockX === resultX && blockY === resultY) ? 'orange' : 'lightcoral';
            });
        });

    const resultText = resultGroup.selectAll('text')
        .data(result.flat().map((d, i) => ({ value: d, index: i })))
        .enter()
        .append('text')
        .attr('x', (d, i) => (i % result[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('y', (d, i) => Math.floor(i / result[0].length) * (cellSize + padding) + cellSize / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .text(d => d.value);

    const animateConvolution = async () => {
        for (let i = 0; i <= dataHeight - kernelHeight; i += step.value) {
            for (let j = 0; j <= dataWidth - kernelWidth; j += step.value) {
                let sum = 0;
                let formula = '';
                for (let ki = 0; ki < kernel.value.length; ki++) {
                    for (let kj = 0; kj < kernel.value[0].length; kj++) {
                        const dataValue = paddedData[i + ki][j + kj];
                        const kernelValue = kernel.value[ki][kj];
                        sum += dataValue * kernelValue;
                        formula += `${dataValue} * ${kernelValue} + `;
                    }
                }
                formula = formula.slice(0, -3);
                result[Math.floor(i / step.value)][Math.floor(j / step.value)] = sum;

                d3.select(formulaContainer.value).text(`公式: ${formula} = ${sum}`);

                resultText.data(result.flat().map((d, i) => ({ value: d, index: i })))
                    .text(d => d.value);

                inputGroup.selectAll('rect')
                    .attr('fill', (d, index) => {
                        const x = index % paddedData[0].length;
                        const y = Math.floor(index / paddedData[0].length);
                        if (x >= j && x < j + kernel.value[0].length && y >= i && y < i + kernel.value.length) {
                            return 'orange';
                        }
                        return 'lightblue';
                    });

                resultGroup.selectAll('rect')
                    .data(result.flat().map((d, i) => ({ value: d, index: i })))
                    .attr('fill', (d, index) => {
                        const x = index % result[0].length;
                        const y = Math.floor(index / result[0].length);
                        if (x === Math.floor(j / step.value) && y === Math.floor(i / step.value)) {
                            return 'orange';
                        }
                        return 'lightcoral';
                    })
                    .attr('stroke', 'black');

                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
    };

    animateConvolution();
};
const startAnimation = () => {
    updateConvolution();
};
onMounted(() => {
    updateConvolution();
});
</script>


<style scoped>
.slider-demo-block {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.demonstration {
    margin-right: 10px;
}

.small-slider {
    width: 200px;
    height: 10px;
}

.el-slider__runway {
    height: 10px !important;
}

.el-slider__thumb {
    width: 14px !important;
    height: 14px !important;
}

.conv-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    width: 100%;
    height: 80vh;
    overflow: auto;
}

.formula-container {
    text-align: center;
    margin-top: 5px;
    font-size: 18px;
    font-weight: bold;
}

/* 新增样式 */
.popover-container {
    position: relative;
}

.popover-content {
    position: absolute;
}
</style>