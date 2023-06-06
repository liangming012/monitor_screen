<template>
  <el-card>
    <template #header>
      <ProfileHeader :return=false></ProfileHeader>
    </template>
    <br>
    <div id="welcome">{{"欢迎您：" + store.userProfile.full_name}}</div>
    <div id="identity">{{"您的身份是：" + identity}}</div>
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
import {computed} from "vue";
const store = useMainStore();
const identity = computed(()=>{
  if(store.userProfile.roles.split(',').indexOf('10001') > -1){
    return '管理员';
  }else if(store.userProfile.roles.split(',').indexOf('10002') > -1){
    return '普通用户';
  }
});
</script>

<style scoped>
#welcome{
  font-size: 4rem;
  color: #6d93ec;
}
#identity{
  font-size: 1rem;
  color: #6d93ec;
}
</style>