<template>
    <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
        <el-radio-button :value="false">expand</el-radio-button>
        <el-radio-button :value="true">collapse</el-radio-button>
    </el-radio-group>
    <el-menu default-active="2" class="el-menu-vertical-demo" :collapse="isCollapse" @open="handleOpen"
        @close="handleClose">
        <el-sub-menu index="1">
            <template #title>
                <el-icon>
                    <svg t="1726279237161" class="icon" viewBox="0 0 1024 1024" version="1.1"
                        xmlns="http://www.w3.org/2000/svg" p-id="3322" width="200" height="200">
                        <path
                            d="M977.4592 676.7616v-102.4h-334.1824a6.6048 6.6048 0 0 0-6.0928 6.0416v95.8976a6.0928 6.0928 0 0 0 5.5808 6.5024h0.512a6.912 6.912 0 0 0 6.5024-5.12c6.0416-30.2592 11.1616-35.3792 23.2448-46.5408 10.752-9.3184 13.5168-14.4384 46.592-14.4384h38.6048a6.0416 6.0416 0 0 1 6.0416 6.0928v232.704q0 40.0384-8.3456 46.5408a43.9296 43.9296 0 0 1-32.6144 13.5168 6.0416 6.0416 0 0 0 0.4608 12.0832h165.2736a6.0416 6.0416 0 0 0 0-12.0832 57.7024 57.7024 0 0 1-34.4576-11.6224 66.2016 66.2016 0 0 1-9.3184-42.8544v-235.9808a6.0416 6.0416 0 0 1 6.0416-6.0416h38.656c34.9184 0 36.7616 4.6592 46.5408 14.4384s16.7424 13.9264 23.2448 46.5408a6.0928 6.0928 0 0 0 6.0928 5.12h2.304a6.5024 6.5024 0 0 0 6.5024-6.5024"
                            fill="#333333" p-id="3323"></path>
                        <path
                            d="M784.4352 354.3552a100.7104 100.7104 0 0 0-71.68 29.6448 105.5744 105.5744 0 0 0-13.7216 17.152l-152.064-152.064a101.3248 101.3248 0 1 0-182.3744-60.7232 103.1168 103.1168 0 0 0 2.2016 20.8384L236.8 256.512a101.376 101.376 0 1 0-50.3808 141.2096l60.6208 102.0416L189.44 588.3904a101.376 101.376 0 1 0 40.96 150.272l135.8848 68.096a97.28 97.28 0 0 0-1.792 18.6368 101.3248 101.3248 0 0 0 202.6496 0 99.9936 99.9936 0 0 0-23.04-64.1024l59.9552-71.68v-45.1584l-81.2544 97.28a100.352 100.352 0 0 0-42.496-16.4864v-161.5872a101.12 101.12 0 0 0 83.6096-75.264l125.0816 1.4336a99.5328 99.5328 0 0 0 18.0736 31.232l-17.9712 21.6576H727.04l1.9968-2.3552a99.7376 99.7376 0 0 0 55.6032 16.64 101.3248 101.3248 0 0 0 0-202.6496z m-537.6-70.6048l130.0992-47.3088A100.8128 100.8128 0 0 0 399.36 264.8064l-73.1648 112.64-82.6368-41.1648a100.7104 100.7104 0 0 0 5.12-32.1024 103.5776 103.5776 0 0 0-2.048-20.4288z m-35.584 99.1232a101.632 101.632 0 0 0 19.3024-20.48l79.872 39.936-46.08 70.6048z m164.5568 396.1856l-132.3008-66.2528a99.6864 99.6864 0 0 0 5.12-32.2048A100.7616 100.7616 0 0 0 213.8624 604.16l49.664-76.8 133.12 223.8976a99.8912 99.8912 0 0 0-20.8384 27.8016z m75.6224-53.9648a99.584 99.584 0 0 0-31.0784 9.6768L281.1392 500.4288l55.296-85.3504 33.2288 16.5888a101.376 101.376 0 0 0 81.92 131.9936z m232.6528-283.0336a86.2208 86.2208 0 0 0-1.024 13.6192c0 1.7408 0 3.4304 0.3072 5.12l-116.3264-1.3312a101.2736 101.2736 0 0 0-184.32-53.7088l-30.2592-15.36 71.2192-109.8752a101.0688 101.0688 0 0 0 102.8096-11.008l160.1024 160.1536a98.304 98.304 0 0 0-2.5088 12.3904z"
                            fill="#333333" p-id="3324"></path>
                    </svg>
                </el-icon>
                <span>卷积</span>
            </template>
            <el-menu-item-group>
                <template #title><span>Group One</span></template>
                <el-menu-item index="1-1">item one</el-menu-item>
                <el-menu-item index="1-2">item two</el-menu-item>
            </el-menu-item-group>
            <el-menu-item-group title="Group Two">
                <el-menu-item index="1-3">item three</el-menu-item>
            </el-menu-item-group>
            <el-sub-menu index="1-4">
                <template #title><span>item four</span></template>
                <el-menu-item index="1-4-1">item one</el-menu-item>
            </el-sub-menu>
        </el-sub-menu>
        <el-menu-item index="2">
            <el-icon><icon-menu /></el-icon>
            <template #title>Navigator Two</template>
        </el-menu-item>
        <el-menu-item index="3" disabled>
            <el-icon>
                <document />
            </el-icon>
            <template #title>Navigator Three</template>
        </el-menu-item>
        <el-menu-item index="4">
            <el-icon>
                <setting />
            </el-icon>
            <template #title>Navigator Four</template>
        </el-menu-item>
    </el-menu>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
} from '@element-plus/icons-vue'

const isCollapse = ref(true)
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}
</style>