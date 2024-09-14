<template>
    <div ref="lineContainer" class="line-container"></div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import * as d3 from 'd3';

const lineContainer = ref(null);

onMounted(() => {
    const width = 800;
    const height = 600;

    const svg = d3.select(lineContainer.value)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // 定义箭头
    svg.append('defs')
        .append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '0 0 10 10')
        .attr('refX', 5)
        .attr('refY', 5)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient', 'auto')
        .append('path')
        .attr('d', 'M 0 0 L 10 5 L 0 10 Z')
        .attr('fill', 'black');

    const line = svg.append('line')
        .attr('x1', 100)
        .attr('y1', 100)
        .attr('x2', 700)
        .attr('y2', 500)
        .attr('stroke', 'black')
        .attr('stroke-width', 2)
        .attr('stroke-dasharray', '5,5')
        .attr('marker-end', 'url(#arrowhead)'); // 应用箭头

    const totalLength = Math.sqrt(Math.pow(700 - 100, 2) + Math.pow(500 - 100, 2));

    const animateLine = () => {
        line.attr('stroke-dashoffset', totalLength)
            .transition()
            .duration(12000) // 减慢速度
            .ease(d3.easeLinear)
            .attr('stroke-dashoffset', 0)
            .on('end', animateLine);
    };

    animateLine();
});
</script>

<style scoped>
.line-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100vh;
}
</style>