<template>
    <div>
        <el-card class="box-card">
          <template #header>
            <ProfileHeader title="修改密码" :user-password=true :return=true></ProfileHeader>
          </template>
            <el-form :model="form" :rules="rules" ref="ruleFormRef" label-position="right" label-width="8rem">
              <el-form-item label="旧密码:" prop="oldPassword">
                <el-input type="password" v-model="form.oldPassword" placeholder="请输入旧密码" />
              </el-form-item>
              <el-form-item label="新密码:" prop="password">
                <el-input type="password" v-model="form.password" placeholder="请输入新密码" />
              </el-form-item>
              <el-form-item label="新密码确认:" prop="passwordVerify">
                <el-input type="password" v-model="form.passwordVerify" placeholder="请再次输入新密码" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit()">提交</el-button>
                <el-button type="primary" @click="resetForm()">重置</el-button>
              </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup lang="ts">
import {useMainStore} from "../../../store/main-store.ts";
import ProfileHeader from "../../../components/profile/ProfileHeader.vue";
import {reactive, ref} from "vue";
const store = useMainStore();
const form = reactive({
  oldPassword: '',
  password: '',
  passwordVerify: '',
});
const validatePassword = (rule, value, callback) => {
  if (value !== form.password) {
    callback(new Error('两次密码输入不一致！'));
  } else {
    callback();
  }
}
const rules = reactive({
  oldPassword: [{ required: true, message: "旧密码不能为空", trigger: "blur"},
    {max:20, message: "密码不能超过20个字符"}],
  password: [{ required: true, message: "新密码不能为空", trigger: "blur"},
    {max:20, message: "密码不能超过20个字符"}],
  passwordVerify: [{ required: true, message: "新密码不能为空", trigger: "blur"},
    {max:20, message: "密码不能超过20个字符"},
    {validator: validatePassword, trigger: "blur"}],
});
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      await store.actionUpdateUserProfile({old_password: form.oldPassword, password: form.password});
    } else {
      return false;
    }
  });
};
const resetForm = () => {   // 重置表单
  if (!ruleFormRef) return;
  ruleFormRef.value.resetFields();
};
</script>

<style scoped>
.el-form-item{
  max-width: 20rem;
}
</style>