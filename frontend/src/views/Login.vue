<template>
  <el-container>
      <el-header>
        <el-icon><Monitor /></el-icon> 监控屏后台管理系统
      </el-header>
      <el-main>
        <el-card>
          <el-form :model="form" :rules="rules" ref="ruleFormRef" label-width="auto">
            <el-form-item label="账号：" prop="email">
              <el-input v-model="form.email" placeholder="请输入账号" @keyup.enter="onSubmit()"/>
            </el-form-item>
            <el-form-item label="密码：" prop="password">
              <el-input type="password" placeholder="请输入密码" v-model="form.password"  @keyup.enter="onSubmit()"/>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit()">登录</el-button>
              <el-button type="primary" @click="resetForm()">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-main>
      <Footer></Footer>
    </el-container>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import {useMainStore} from "../store/main-store";
import {isEmail} from "../utils/validate/validate";
import Footer from "../components/Footer.vue";
const form = reactive({
  email: "",
  password: "",
});
// trigger为blur光标离开时检查，change变化时检查
const rules = reactive({
  email: [{ required: true, message: "账号不能为空", trigger: "blur" },
    {type: 'email', message: "账号必须是邮箱格式", trigger: "blur"}],
  // email: [{ required: true, validator: isEmail, trigger: "blur" }], //自定义表单验证
  password: [{ required: true, message: "密码不能为空", trigger: "blur" }],
});
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      const store = useMainStore();
      await store.actionLogIn({username: form.email, password: form.password});
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
.el-footer {
  height: 10%;
  text-align: center;
}
</style>
