<template>
  <div class="model-viewer">
    <VueFlow fit-view-on-init class="my-flow" v-model="elements" @node-click="onNodeClick">
      <Background />
      <Panel :position="PanelPosition.TopRight">
      </Panel>
      <Controls />
    </VueFlow>
    <el-drawer
      title="节点详情"
      :model-value="drawerVisible"
      direction="rtl"
      size="30%"
      @close="drawerVisible = false"
    >
      <p><strong>名称:</strong> {{ selectedNode?.data.label }}</p>
      <p><strong>类型:</strong> {{ selectedNode?.type }}</p>
      <p><strong>位置:</strong> ({{ selectedNode?.position.x }}, {{ selectedNode?.position.y }})</p>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import '@vue-flow/core/dist/style.css';
import '@vue-flow/core/dist/theme-default.css';
import 'element-plus/dist/index.css';

import { ref, onMounted } from 'vue'
import { Background, Panel, PanelPosition, Controls } from '@vue-flow/additional-components'
import { VueFlow, useVueFlow } from '@vue-flow/core'
import axios from 'axios'
import { ElDrawer } from 'element-plus'

const modelLayers = ref([])

const fetchModelStructure = async () => {
  try {
    const response = await axios.get('../../vis/model_structure.json')
    const modelParam = response.data
    modelLayers.value = modelParam

    const nodes = []
    const edges = []

    Object.entries(modelParam).forEach(([name, layer], index) => {
      let nodeType = 'default'
      if (index === 0) {
        nodeType = 'input'
      } else if (index === Object.keys(modelParam).length - 1) {
        nodeType = 'output'
      } else {
        nodeType = 'default'
      }

      nodes.push({
        id: `${index + 1}`,
        type: nodeType,
        data: { label: name },
        position: { x: 100, y: 100 * (index + 1) }
      })

      if (index > 0) {
        edges.push({
          id: `e${index}-${index + 1}`,
          source: `${index}`,
          target: `${index + 1}`,
          animated: true
        })
      }
    })

    elements.value = [...nodes, ...edges]
  } catch (error) {
    console.error('Error fetching model structure:', error)
  }
}

onMounted(() => {
  fetchModelStructure()
})

const elements = ref([])
const drawerVisible = ref(false)
const selectedNode = ref(null)

const onNodeClick = (event) => {
  console.log('Node clicked:', event.node) // 添加日志以调试
  selectedNode.value = event.node
  drawerVisible.value = true
}
</script>

<style scoped>
.model-viewer {
  width: 100%;
  height: 100vh; /* 设置为视口高度的 100% */
}

.my-flow {
  width: 100%;
  height: 100%;
}
</style>