<template>
  <div class="model-viewer">
    <VueFlow fit-view-on-init class="my-flow" v-model="elements">
      <Background />
      <Panel :position="PanelPosition.TopRight">
      </Panel>
      <Controls />
    </VueFlow>
  </div>
</template>

<script setup lang="ts">
import '@vue-flow/core/dist/style.css';
import '@vue-flow/core/dist/theme-default.css';

import { ref } from 'vue'
import { Background, Panel, PanelPosition, Controls } from '@vue-flow/additional-components'
import { VueFlow, useVueFlow } from '@vue-flow/core'

const data = [
  { id: '1', type: 'input', label: 'Node 1', position: { x: 250, y: 5 } },
  { id: '2', label: 'Node 2', position: { x: 100, y: 100 } },
  { id: '3', label: 'Node 3', position: { x: 400, y: 100 } },
  { id: '4', label: 'Node 4', position: { x: 400, y: 200 } },
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e1-3', source: '1', target: '3',animated: true },
]
let elements = ref(data)

let { onPaneReady, onNodeDragStop, onConnect, addEdges } = useVueFlow()

onPaneReady(({ fitView }) => {
  fitView()
})
onNodeDragStop((e) => console.log('drag stop', e))
onConnect((params) => addEdges([params]))

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