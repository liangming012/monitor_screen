<template>
  <el-row type="flex" justify="space-between">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item><router-link to="/main/screen/list">屏幕管理</router-link></el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.list">屏幕列表</el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.add">添加屏幕</el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.edit">编辑屏幕</el-breadcrumb-item>
    </el-breadcrumb>
    <el-button v-if="props.return" style="float:right" @click="router.push({name: 'screens', query: router.currentRoute.value.query})">返回</el-button>
  </el-row>
</template>
<script setup lang="ts">
import router from "../../router";

//支持配置字段 type 类型，required 是否必填，default默认值，validator 校验
const props = defineProps({
  return: {
    type: Boolean,
    require: true,
    default: false,
  },
  list: {
    type: Boolean,
    require: true,
    default: false
  },
  add: {
    type: Boolean,
    require: true,
    default: false
  },
  edit: {
    type: Boolean,
    require: true,
    default: false
  }
});
</script>
<style scoped>
</style>
