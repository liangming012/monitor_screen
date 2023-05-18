<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <ShowHeader :edit=true :return=true></ShowHeader>
      </template>
      <el-form :model="form" :rules="rules" ref="ruleFormRef"  label-position="right" label-width="8rem">
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
        <el-form-item label="构建ID:" prop="buildId">
          <el-input type="number" v-model.trim="form.buildId" placeholder="请输入构建ID" />
        </el-form-item>
        <el-form-item label="持续时间:" prop="duration">
          <el-input type="number" v-model.trim="form.duration" placeholder="请输入持续时间" />
        </el-form-item>
        <el-form-item label="构建 URL:" prop="url">
          <el-input v-model="form.url" placeholder="请输入构建 URL"/>
        </el-form-item>
        <el-form-item label="检查时间:" prop="checkTime">
          <el-date-picker
              v-model="form.checkTime"
              type="datetime"
              placeholder="请选择检查时间"
              :shortcuts="shortcuts"
          />
        </el-form-item>
        <el-form-item label="状态:" prop="status">
          <el-select v-model="form.status">
            <el-option
                v-for="statu in status"
                :key="statu.id"
                :label="statu.name"
                :value="statu.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit()">提交</el-button>
          <el-button type="primary" @click="resetForm()">重置</el-button>
        </el-form-item>
      </el-form>

    </el-card>
  </div>
</template>

<script setup>
import {onMounted, reactive, ref} from "vue";
import {project} from "../../../api/project.ts";
import {ElMessage} from "element-plus";
import router from "../../../router/index.ts";
import {record as api} from "../../../api/record.ts";
import ShowHeader from "../../../components/show/ShowHeader.vue";
let projects = ref([]);
const status = [
  {"id": 0, "name": '成功'},
  {"id": 1, "name": '失败'},
  {"id": 2, "name": '超时'},
  {"id": 9999, "name": '失效'},
]
const shortcuts = [
  {
    text: '今天',
    value: new Date(),
  },
  {
    text: '昨天',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() - 3600 * 1000 * 24)
      return date
    },
  },
  {
    text: '一周前',
    value: () => {
      const date = new Date()
      date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
      return date
    },
  },
]

const form = reactive({
  buildId: null,
  duration: 0,
  status: null,
  url: '',
  checkTime: null,
  projectId: '',
});

const rules = reactive({
  buildId: [{ required: true, message: "构建ID不能为空", trigger: "blur"}],
  duration: [{ required: true, message: "持续时间不能为空", trigger: "blur" }],
  status: [{ required: true, message: "状态必须选择", trigger: "blur"},],
  url: [{ required: true, message: "构建地址不能为空", trigger: "blur"},
    { pattern: /^https?:\/\/.+$/, message: "构建地址必须http://或https://开头", trigger: "blur" },
    {max:500, message: "构建地址不能超过500个字符"}],
  checkTime: [{ required: true, message: "检查时间不能为空", trigger: "blur"}],
  projectId: [{ required: true, message: "项目必须选择", trigger: "blur"}],
});
// 获取列表
const getProjects = async () => {
  const res = await project.getList();
  projects.value = res.data;
}

onMounted(() => {
  getProjects();
  getProject();})
const props = defineProps({id:String});
const getProject = async () => {
  const res = await api.getRecord(props.id);
  form.buildId = res.data.build_id;
  form.duration = res.data.duration;
  form.status = res.data.status;
  form.url = res.data.url;
  form.checkTime = new Date(res.data.check_time*1000);
  form.projectId = res.data.project_id.toString();
}
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      const response = await api.updateRecord(
          props.id,
          {build_id: form.buildId,
            duration: form.duration,
            status: form.status,
            url: form.url,
            check_time: form.checkTime.getTime()/1000,
            project_id: form.projectId,
          });
      if (response.data) {
        await router.push({name:'records', query: router.currentRoute.value.query})
        ElMessage.success('编辑记录成功！');
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
  max-width: 30rem;
}
</style>