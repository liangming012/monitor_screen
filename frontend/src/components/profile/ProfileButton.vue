<template>
  <el-button v-if="props.view" type="primary" @click="router.push({name: 'profileView'})">查看个人信息</el-button>
  <el-button v-if="props.edit" type="primary" @click="router.push({name: 'profileEdit'})">修改个人信息</el-button>
  <el-button v-if="props.password" type="primary" @click="router.push({name: 'profilePassword'})">修改密码</el-button>
</template>
<script setup lang="ts">
import router from "../../router";

//支持配置字段 type 类型，required 是否必填，default默认值，validator 校验
const props = defineProps({
  view: {
    type: Boolean,
    require: true,
    default: true,
    // validator: (value) => {
    //   return value > 1;
    // },
  },
  edit: {
    type: Boolean,
    require: true,
    default: true,
  },
  password: {
    type: Boolean,
    require: true,
    default: true,
  },
});
</script>
<style scoped>
</style>
