<template>
    <div>
        <el-container class="home-container">
            <!-- header -->
            <el-header>
                <el-row>
                    <el-col :span="1">
                      <div class="toggle-button" @click="isCollapse = !isCollapse">
                        <el-icon :size="60">
                          <Expand v-if="isCollapse" />
                          <Fold v-if="!isCollapse" />
                        </el-icon>
                      </div>
                    </el-col>
                    <el-col :offset="0" :span="3">
                        <p class="system-name">监控屏管理系统</p>
                    </el-col>
                    <el-col :offset="14" :span="6">
                        <el-dropdown>
                          <p>
                            <el-button type="primary">
                              {{store.userProfile.full_name}}<el-icon class="el-icon--right"><arrow-down /></el-icon>
                            </el-button>
                          </p>
                          <template #dropdown>
                              <el-dropdown-menu>
                                <el-dropdown-item @click.native="router.push('/main/profile/view')">个人信息</el-dropdown-item>
                                  <el-dropdown-item @click.native="logout">退出系统</el-dropdown-item>
                              </el-dropdown-menu>
                          </template>
                        </el-dropdown>
                    </el-col>
                </el-row>
            </el-header>
            <el-container style="overflow: auto">
                <!-- 菜单 -->
                <el-aside>
                    <el-menu :router=true :default-active="router.currentRoute.value.path" class="el-menu-vertical-demo" :collapse="isCollapse">
                      <el-menu-item index="/main/dashboard">
                          <el-icon>
                              <house />
                          </el-icon>
                          <span>首页</span>
                      </el-menu-item>
                      <el-menu-item index="/main/user/list">
                        <el-icon><user /></el-icon>
                        <template #title>用户管理</template>
                      </el-menu-item>
                      <el-sub-menu index="/projects">
                          <template #title>
                            <el-icon><Operation /></el-icon>
                            <span>项目管理</span>
                          </template>
                          <el-menu-item index="2-1">项目列表</el-menu-item>
                          <el-menu-item index="2-1">记录列表</el-menu-item>
                      </el-sub-menu>
                      <el-sub-menu index="/screens">
                        <template #title>
                          <el-icon><Monitor /></el-icon>
                          <span>屏幕管理</span>
                        </template>
                        <el-menu-item index="2-1">屏幕列表</el-menu-item>
                        <el-menu-item index="2-1">显示列表</el-menu-item>
                      </el-sub-menu>
                      <el-sub-menu index="/notices">
                        <template #title>
                          <el-icon><Notification /></el-icon>
                          <span>报警管理</span>
                        </template>
                        <el-menu-item index="2-1">报警方式</el-menu-item>
                        <el-menu-item index="2-1">报警列表</el-menu-item>
                      </el-sub-menu>
                    </el-menu>
                </el-aside>
                <el-container>
                    <el-main>
                        <!-- 面包屑 -->
                        <!-- <Breadcrumb /> -->
                        <!-- 主要内容 -->
                        <router-view></router-view>
                    </el-main>
                </el-container>
            </el-container>
          <Footer></Footer>
        </el-container>
    </div>
</template>
<script setup>
import { onBeforeMount, ref } from 'vue';
import {useMainStore} from "../../store/main-store.ts";
import router from "../../router/index.ts";
import Footer from "../../components/Footer.vue";
const store = useMainStore();
let isCollapse = ref(false); //默认展开菜单

const logout = () => {
    store.actionLogOut()
}
</script>

<style scoped>
.home-container {
  position: absolute;
  height: 100%;
  top: 0px;
  left: 0px;
  width: 100%;
  background: #f2f3f5;
}
.el-header {
  background: #2661ef;
  padding: 0 10px;
  overflow: hidden;
}
.toggle-button {
  height: 100%;
  background-color: #2661ef;
  top:60%;
  text-align: center;
  cursor: pointer;
  color: black;
}
.system-name {
  color: #fff;
  font-size: 1rem;
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 10rem;
  min-height: 20rem;
}
.el-aside {
  background: white;
  width: auto !important;
}
</style>