<template>
  <el-card>
    <el-container>
      <el-header>
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/main/dashboard' }">首页</el-breadcrumb-item>
        </el-breadcrumb>
      </el-header>
      <el-main>
        <el-row>
          欢迎 {{store.userProfile.full_name}} ！
        </el-row>
        <br>
        <br>
        <br>
        <br>
        <el-row>
          <el-button type="primary">查看个人信息</el-button>
          <el-button type="primary">修改个人信息</el-button>
          <el-button type="primary">修改密码</el-button>
        </el-row>
      </el-main>
    </el-container>
  </el-card>
</template>
<script setup>
import {useMainStore} from "../../store/main-store.ts";
const store = useMainStore();
</script>

<style scoped>

</style>