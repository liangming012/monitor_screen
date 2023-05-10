<template>
  <el-row type="flex" justify="space-between">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item><router-link to="/main/dashboard">用户管理</router-link></el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.userList">用户列表</el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.userAdd">添加用户</el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.userEdit">编辑用户</el-breadcrumb-item>
    </el-breadcrumb>
    <el-button v-if="props.return" style="float:right" @click="router.push('/main/user/list')">返回</el-button>
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
  userList: {
    type: Boolean,
    require: true,
    default: false
  },
  userAdd: {
    type: Boolean,
    require: true,
    default: false
  },
  userEdit: {
    type: Boolean,
    require: true,
    default: false
  }
});
</script>
<style scoped>
</style>
