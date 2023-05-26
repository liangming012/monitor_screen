<template>
  <el-container>
  123
  </el-container>
</template>

<script setup lang="ts">
import {view} from "../api/view.ts";
import {onMounted} from "vue";
import router from "../router/index.ts";
import {getLastItem} from "../utils/common";

onMounted(() => {
  getViewData();
});
const getViewData = async () => {
  const res = await view.getViewData(getLastItem(router.currentRoute.value.path));
  console.log(res.data);
}
</script>

<style scoped>

</style>
