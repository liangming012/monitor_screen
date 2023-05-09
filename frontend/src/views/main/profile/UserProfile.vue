<template>
    <div>
        <el-card class="box-card">
          <template #header>
            <ProfileHeader title="个人信息" :user-view=true></ProfileHeader>
          </template>
          <el-form>
              <el-form-item label="姓名:">
                  {{ store.userProfile.full_name }}
              </el-form-item>
              <el-form-item label="邮箱:">
                  {{ store.userProfile.email }}
              </el-form-item>
          </el-form>
          <ProfileButton :view=false></ProfileButton>
        </el-card>
    </div>
</template>

<script setup>
import {useMainStore} from "../../../store/main-store.ts";
import ProfileButton from "../../../components/profile/ProfileButton.vue";
import ProfileHeader from "../../../components/profile/ProfileHeader.vue";
const store = useMainStore();
</script>

<style scoped>
</style>