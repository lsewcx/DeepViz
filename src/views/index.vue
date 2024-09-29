<template>
  <div class="model-viewer">
    <VueFlow fit-view-on-init class="my-flow" v-model="elements" @node-click="onNodeClick">
      <Background />
      <Panel :position="PanelPosition.TopRight">
      </Panel>
      <Controls />
    </VueFlow>
    <el-drawer title="节点详情" :model-value="drawerVisible" direction="rtl" size="30%" @close="drawerVisible = false">
      <el-descriptions v-if="nodeDetails" border :column="1">
        <el-descriptions-item label="名称">
          {{ selectedNode?.data.label }}
        </el-descriptions-item>
        <el-descriptions-item label="类型">
          {{ nodeDetails.type }}
        </el-descriptions-item>
        <template v-for="(value, key) in nodeDetails.parameters" :key="key">
          <el-descriptions-item v-if="key !== 'bias'" :label="key">
            {{ Array.isArray(value) ? value.join(', ') : value }}
          </el-descriptions-item>
          <el-descriptions-item v-else :label="key">
            <el-collapse>
              <el-collapse-item title="点击展开">
                {{ value.join(', ') }}
              </el-collapse-item>
            </el-collapse>
          </el-descriptions-item>
        </template>
      </el-descriptions>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import '@vue-flow/core/dist/style.css';
import '@vue-flow/core/dist/theme-default.css';
import 'element-plus/dist/index.css';

import { ref, onMounted } from 'vue'
import { Background, Panel, PanelPosition, Controls } from '@vue-flow/additional-components'
import { VueFlow } from '@vue-flow/core'
import axios from 'axios'
import { ElDrawer, ElDescriptions, ElDescriptionsItem, ElCollapse, ElCollapseItem } from 'element-plus'

const modelLayers = ref([])

const fetchModelStructure = async () => {
  try {
    const response = await axios.get('../../vis/model_structure.json')
    const modelParam = response.data
    modelLayers.value = modelParam

    const nodes: { id: string; type: string; data: { label: string; }; position: { x: number; y: number; }; }[] = []
    const edges: { id: string; source: string; target: string; animated: boolean; }[] = []

    Object.entries(modelParam).forEach(([name], index) => {
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

const elements = ref<Array<{ id: string; type?: string; data?: { label: string; }; position?: { x: number; y: number; }; source?: string; target?: string; animated?: boolean; }>>([])
const drawerVisible = ref(false)
const selectedNode = ref<{ data: { label: any; } } | null>(null)
const nodeDetails = ref(null)

const onNodeClick = (event: { node: { data: { label: any; }; } | null; }) => {
  console.log('Node clicked:', event.node) // 添加日志以调试
  selectedNode.value = event.node
  drawerVisible.value = true

  // 获取节点详细信息
  const nodeName = event.node.data.label
  nodeDetails.value = modelLayers.value[nodeName]
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