<template>
  <el-container class="home-container">
      <!-- header -->
      <el-header>
          <el-row>
              <el-col :span="1">
                <div class="toggle-button" @click="isCollapse = !isCollapse">
                  <el-icon :size="50">
                    <Expand v-if="isCollapse" />
                    <Fold v-if="!isCollapse" />
                  </el-icon>
                </div>
              </el-col>
              <el-col :span="2">
                  <p class="system-name">监控屏管理</p>
              </el-col>
              <el-col :offset="17" :span="4">
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
              <el-menu :router=true :default-active="store.activeMenu" class="el-menu-vertical-demo" :collapse="isCollapse">
                <template v-for="menu in store.menuData" :key="menu.id">
                  <!-- 如果没有子菜单-->
                  <el-menu-item v-if="menu.children.length === 0" :index="menu.index">
                    <i class="el-icon">
                      <component v-if="menu.icon" :is="menu.icon"></component>
                    </i>
                    <span>{{menu.name}}</span>
                  </el-menu-item>
                  <!-- 如果有子菜单-->
                  <el-sub-menu v-if="menu.children.length > 0" :index="menu.index">
                    <template #title>
                      <i class="el-icon">
                        <component v-if="menu.icon" :is="menu.icon"></component>
                      </i>
                      <span>{{menu.name}}</span>
                    </template>
                    <el-menu-item v-for="childMenu in menu.children"  :key="childMenu.id"  :index="childMenu.index">
                      <i class="el-icon">
                        <component v-if="childMenu.icon" :is="childMenu.icon"></component>
                      </i>
                      <span>{{childMenu.name}}</span>
                    </el-menu-item>
                  </el-sub-menu>
                </template>
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
</template>
<script setup lang="ts">
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
  background: #5a87f5;
  padding: 0 10px;
  overflow: hidden;
}
.toggle-button {
  height: 100%;
  background-color: #5a87f5;
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