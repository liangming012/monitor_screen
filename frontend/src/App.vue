<template>
  <div v-loading.fullscreen.lock="store.isLoading">
    <router-view></router-view>
  </div>
</template>
<script setup lang="ts">
import {useMainStore} from "./store/main-store";

const store = useMainStore();
</script>
<style scoped>
</style>
