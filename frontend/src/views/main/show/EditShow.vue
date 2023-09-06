<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <ShowHeader :edit=true :return=true></ShowHeader>
      </template>
      <el-form :model="form" :rules="rules" ref="ruleFormRef" label-position="right" label-width="8rem">
        <el-form-item label="屏幕名称:" prop="screenId">
          <el-select v-model="form.screenId">
            <el-option
                v-for="screen in screens"
                :key="screen.id.toString()"
                :label="screen.name"
                :value="screen.id.toString()"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="项目名称:" prop="projectId">
          <el-select v-model="form.projectId">
            <el-option
                v-for="project in projects"
                :key="project.id.toString()"
                :label="project.name"
                :value="project.id.toString()"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="显示权重:" prop="weight">
          <el-input type="number" v-model.trim="form.weight" placeholder="请输入显示权重"/>
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
import {onMounted, reactive, ref} from "vue";
import {project} from "../../../api/project.ts";
import {screen} from "../../../api/screen.ts";
import {ElMessage} from "element-plus";
import router from "../../../router/index.ts";
import {show as api} from "../../../api/show.ts";
import ShowHeader from "../../../components/show/ShowHeader.vue";

let projects = ref([]);
let screens = ref([]);
const form = reactive({
  screenId: '',
  weight: 0,
  projectId: '',
});

const rules = reactive({
  screenId: [{required: true, message: "屏幕必须选择", trigger: "blur"}],
  weight: [{required: true, message: "权重不能为空", trigger: "blur"},
    {pattern: /^[0-9]*$/, message: "权重必须为数字", trigger: "blur"}],
  projectId: [{required: true, message: "项目必须选择", trigger: "blur"}],
});
// 获取列表
const getProjects = async () => {
  const res = await project.getList();
  projects.value = res.data;
}
const getScreens = async () => {
  const res = await screen.getList();
  screens.value = res.data;
}
onMounted(() => {
  getProjects();
  getScreens();
  getShow();
});
const props = defineProps({id: String});
const getShow = async () => {
  const res = await api.getShow(props.id);
  form.screenId = res.data.screen_id.toString();
  form.weight = res.data.weight;
  form.projectId = res.data.project_id.toString();
}
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      const response = await api.updateShow(
          props.id,
          {
            screen_id: form.screenId,
            weight: form.weight,
            project_id: form.projectId,
          });
      if (response.data) {
        await router.push({name: 'shows', query: router.currentRoute.value.query})
        ElMessage.success('编辑显示项目成功！');
      } else {
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
.el-form-item {
  max-width: 20rem;
}
</style>