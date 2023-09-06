<template>
  <el-row type="flex" justify="space-between">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item><router-link to="/main/project/list">项目管理</router-link></el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.list">项目列表</el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.add">添加项目</el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.edit">编辑项目</el-breadcrumb-item>
    </el-breadcrumb>
    <el-button v-if="props.return" style="float:right" @click="router.push({name: 'projects', query: router.currentRoute.value.query})">返回</el-button>
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
