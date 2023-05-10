<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <UserHeader :user-add=true :return=true></UserHeader>
      </template>


    </el-card>
  </div>
</template>

<script setup>
import UserHeader from "../../../components/user/UserHeader.vue";

</script>

<style scoped>
</style>