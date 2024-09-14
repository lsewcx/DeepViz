<script setup lang="ts">
import asidebar from './components/menu/asidebar.vue';
import headerbar from './components/menu/headerbar.vue';
</script>

<template>
    <div class="common-layout">
        <el-container>
            <el-header><headerbar></headerbar></el-header>
            <el-container>
                <el-aside width="200px"><asidebar></asidebar></el-aside>
                <el-container>
                    <el-main>    <RouterView /></el-main>
                    <!-- <el-footer>Footer</el-footer> -->
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>

<style scoped>
</style>
