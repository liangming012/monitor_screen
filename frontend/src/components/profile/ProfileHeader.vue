<template>
  <el-row type="flex" justify="space-between">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item><router-link to="/main/dashboard">首页</router-link></el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.userView">个人信息</el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.userEdit">修改信息</el-breadcrumb-item>
      <el-breadcrumb-item v-if="props.userPassword">修改密码</el-breadcrumb-item>
    </el-breadcrumb>
    <span>{{props.title}}</span>
    <el-button v-if="props.return" style="float:right" @click="router.push({name: 'main'})">返回</el-button>
  </el-row>
</template>
<script setup lang="ts">
import router from "../../router";

//支持配置字段 type 类型，required 是否必填，default默认值，validator 校验
const props = defineProps({
  title: {
    type: String,
    require: true,
    default: '',
  },
  return: {
    type: Boolean,
    require: true,
    default: false,
  },
  userView: {
    type: Boolean,
    require: true,
    default: false
  },
  userEdit: {
    type: Boolean,
    require: true,
    default: false
  },
  userPassword: {
    type: Boolean,
    require: true,
    default: false
  },
});
</script>
<style scoped>
</style>
