<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <ProjectHeader :add=true :return=true></ProjectHeader>
      </template>
      <el-form :model="form" :rules="rules" ref="ruleFormRef"  label-position="right" label-width="8rem">
        <el-form-item label="项目名称:" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="持续时间:" prop="durationLimit">
          <el-input v-model.trim="form.durationLimit" placeholder="请输入持续时间" />
        </el-form-item>
        <el-form-item label="Jenkins URL:" prop="jenkinsUrl">
          <el-input v-model="form.jenkinsUrl" placeholder="请输入Jenkins URL"/>
        </el-form-item>
        <el-form-item label="是否启用:" prop="enable">
          <el-switch v-model="form.enable"/>
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
import {reactive, ref} from "vue";
import {project as api} from "../../../api/project.ts";
import {ElMessage} from "element-plus";
import router from "../../../router/index.ts";
import ProjectHeader from "../../../components/project/ProjectHeader.vue";
import {minNumber} from "../../../utils/validate/validate";
const form = reactive({
  name: '',
  durationLimit: '',
  jenkinsUrl: '',
  enable: false,
});
const rules = reactive({
  name: [{ required: true, message: "项目名称不能为空", trigger: "blur"},
    {max:50, message: "项目名称不能超过50个字符"}],
  durationLimit: [{ required: true, message: "持续时间不能为空", trigger: "blur" },
    { pattern: /^[0-9]*$/, message: "持续时间必须为数字", trigger: "blur" },
    { validator: minNumber, min: 1, trigger: "blur" }],
  jenkinsUrl: [{ required: true, message: "Jenkins地址不能为空", trigger: "blur"},
    { pattern: /^https?:\/\/.+$/, message: "Jenkins地址必须http://或https://开头", trigger: "blur" },
    {max:500, message: "jenkins地址不能超过500个字符"}],
});
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      const response = await api.createProject(
          {name: form.name,
                enable: form.enable,
                duration_limit: form.durationLimit,
                jenkins_url: form.jenkinsUrl,
          });
      if (response.data) {
        await router.push({name:'projects', query: router.currentRoute.value.query})
        ElMessage.success('添加项目成功！');
      }else {
        ElMessage.error(response.data.detail);
      }
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