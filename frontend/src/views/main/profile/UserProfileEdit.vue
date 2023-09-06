<template>
    <div>
        <el-card class="box-card">
          <template #header>
            <ProfileHeader title="修改信息" :user-edit=true :return=true></ProfileHeader>
          </template>
            <el-form :model="form" :rules="rules" ref="ruleFormRef"  label-position="right" label-width="8rem">
              <el-form-item label="姓名:" prop="fullName">
                <el-input v-model="form.fullName" placeholder="请输入用户名" />
              </el-form-item>
              <el-form-item label="邮箱:" prop="email">
                <el-input v-model="form.email" placeholder="请输入邮箱" />
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
  fullName: store.userProfile.full_name,
  email: store.userProfile.email,
});
const rules = reactive({
  fullName: [{ required: true, message: "姓名不能为空", trigger: "blur"},
    {max:50, message: "姓名不能超过50个字符"}],
  email: [{ required: true, message: "邮箱不能为空", trigger: "blur" },
    {type: 'email', message: "必须是邮箱格式", trigger: "blur"}],
});
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      await store.actionUpdateUserProfile({full_name: form.fullName, email: form.email});
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