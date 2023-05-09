<template>
  <el-card>
    <template #header>
      <ProfileHeader :title=title :return=false></ProfileHeader>
    </template>
    <br>
    <br>
    <br>
    <br>
    <ProfileButton></ProfileButton>
  </el-card>
</template>
<script setup>
import {useMainStore} from "../../store/main-store.ts";
import ProfileButton from "../../components/profile/ProfileButton.vue";
import ProfileHeader from "../../components/profile/ProfileHeader.vue";
const store = useMainStore();
const title = "欢迎 " + store.userProfile.full_name + ' !';


</script>

<style scoped>

</style>