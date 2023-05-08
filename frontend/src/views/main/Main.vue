<template>
    <div>
        <el-container class="home-container">
            <!-- header -->
            <el-header>
                <el-row>
                    <el-col :span="4">
                        <p class="system-name">监控屏管理系统</p>
                    </el-col>
                    <el-col :offset="12" :span="8">
                        <el-dropdown>
                            <span class="el-dropdown-link">
                                姓名 &nbsp;&nbsp; <el-icon class="el-icon--right">
                                    <arrow-down />
                                </el-icon>
                            </span>
                            <template #dropdown>
                                <el-dropdown-menu>
                                  <el-dropdown-item @click.native="">个人信息</el-dropdown-item>
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
                    <div class="toggle-button" @click="isCollapse = !isCollapse">
                        <el-icon :size="20">
                            <Expand v-if="isCollapse" />
                            <Fold v-if="!isCollapse" />
                        </el-icon>
                    </div>
                    <el-menu router :default-active="activePath" class="el-menu-vertical-demo" :collapse="isCollapse">
                        <el-menu-item index="/index" @click="saveActiveNav('/index')">
                            <el-icon>
                                <house />
                            </el-icon>
                            <span>首页</span>
                        </el-menu-item>
                        <el-sub-menu index="1">
                            <template #title>
                                <el-icon>
                                    <Setting />
                                </el-icon>
                                <span>系统设置</span>
                            </template>
                            <el-menu-item index="2-1">权限管理</el-menu-item>
                        </el-sub-menu>
                        <el-menu-item index="/user/list" @click="saveActiveNav('/user/list')">
                            <el-icon>
                                <user />
                            </el-icon>
                            <span>用户管理</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-container>
                    <el-main>
                        <!-- 面包屑 -->
                        <!-- <Breadcrumb /> -->
                        <!-- 主要内容 -->
                        <router-view></router-view>
                    </el-main>
                    <el-footer>
                      <p>Copyright © 2023-2033 <el-tag>作者邮箱：liangming012@gmail.com</el-tag></p>
                    </el-footer>
                </el-container>
            </el-container>
        </el-container>
    </div>
</template>
<script setup>
import { onBeforeMount, ref } from 'vue';
import { useRouter } from 'vue-router'
import {useMainStore} from "../../store/main-store.ts";
const router = useRouter();
// 挂载 DOM 之前
onBeforeMount(() => {
    activePath.value = sessionStorage.getItem("activePath")
        ? sessionStorage.getItem("activePath")
        : "/index"
})
let isCollapse = ref(false);
let activePath = ref("");
// 保存链接的激活状态
const saveActiveNav = (path) => {
    sessionStorage.setItem("activePath", path);
    activePath.value = path;
}
const logout = () => {
    // 清除缓存
    const store = useMainStore();
    store.actionLogOut()

}
</script>

<style scoped>
</style>