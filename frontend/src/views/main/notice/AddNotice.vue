<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <NoticeHeader :add=true :return=true></NoticeHeader>
      </template>
      <el-form :model="form" :rules="rules" ref="ruleFormRef"  label-position="right" label-width="8rem">
        <el-form-item label="报警群组名称:" prop="name">
          <el-input v-model="form.name" placeholder="请输入报警群组名称" />
        </el-form-item>
        <el-form-item label="报警方式:" prop="noticeType">
          <el-checkbox-group v-model="form.noticeType">
            <el-checkbox label="钉钉" />
            <el-checkbox label="飞书" />
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="webhook url:" prop="webhookUrl">
          <el-input v-model="form.webhookUrl" placeholder="请输入webhook url"/>
        </el-form-item>
        <el-form-item label="报警@所有人:" prop="atAll">
          <el-switch v-model="form.atAll"/>
        </el-form-item>
        <el-form-item label="监控方式:" prop="watchType">
          <el-radio-group v-model="form.watchType">
            <el-radio label="1">按屏幕</el-radio>
            <el-radio label="2">按项目</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="form.watchType === '1'" label="监控的屏幕:" prop="screenIds">
          <el-select-v2
              style="width: 100%"
              v-model="form.screenIds"
              :options="screens"
              placeholder="请选择要监控的屏幕"
              multiple
              clearable
          />
        </el-form-item>
        <el-form-item v-if="form.watchType === '2'" label="监控的项目:" prop="projectIds">
          <el-select-v2
              style="width: 100%"
              v-model="form.projectIds"
              :options="projects"
              placeholder="请选择要监控的项目"
              multiple
              clearable
          />
        </el-form-item>
        <el-form-item label="失败报警阈值:" prop="faildCount">
          <el-input type="number" :rows="3" v-model="form.faildCount" placeholder="请输入报警阈值" max="999" min="1">
            <template #append>次</template>
          </el-input>
        </el-form-item>
        <el-form-item label="超时报警阈值:" prop="timeOutCount">
          <el-input type="number" :rows="3" v-model="form.timeOutCount" placeholder="请输入报警阈值" max="999" min="1">
            <template #append>次</template>
          </el-input>
        </el-form-item>
        <el-form-item label="备注信息:" prop="remarks">
          <el-input type="textarea" :rows="3" v-model="form.remarks" placeholder="请输入备注信息" />
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
import {ElMessage} from "element-plus";
import router from "../../../router/index.ts";
import {screen} from "../../../api/screen.ts";
import NoticeHeader from "../../../components/notice/NoticeHeader.vue";
import {project} from "../../../api/project.ts";
import {notice as api} from "../../../api/notice.ts";
import {isEmptyArray} from "../../../utils/validate/validate";
const projects = ref([]);
const screens = ref([]);
onMounted(() => {
  getProjects();
  getScreens();
});
// 获取列表
const getProjects = async () => {
  const res = await project.getList();
  projects.value = res.data.map(({name: label, id: value, ...rest}) => ({label,value, ...rest}));
}
const getScreens = async () => {
  const res = await screen.getList();
  // [{name:'value1', id:'value2'}, .. ] 替换key，变成 [{label:'value1', value:'value2'}, .. ]
  screens.value = res.data.map(({name: label, id: value, ...rest}) => ({label,value, ...rest}));
}
const form = reactive({
  name: '',
  noticeType: [],
  webhookUrl: '',
  atAll: false,
  remarks: '',
  watchType: '1',
  screenIds: [],
  projectIds: [],
  faildCount: 1,
  timeOutCount: 1,
});
const rules = reactive({
  name: [{ required: true, message: "报警群组名称不能为空", trigger: "blur"},
    {max:50, message: "报警群组名称不能超过50个字符"}],
  webhookUrl: [{ required: true, message: "webhook url不能为空", trigger: "blur"},
    { pattern: /^https?:\/\/.+$/, message: "webhook url必须http://或https://开头", trigger: "blur" },
    {max:500, message: "webhook url不能超过500个字符"}],
  remarks: [{max:500, message: "备注信息不能超过500个字符"}],
  screenIds: [{ required: true, validator: isEmptyArray, trigger: "change" }], //自定义表单验证
  projectIds: [{ required: true, validator: isEmptyArray, trigger: "change" }], //自定义表单验证
  faildCount: [{ required: true, message: "失败报警阈值不能为空", trigger: "blur"},],
  timeOutCount: [{ required: true, message: "超时报警阈值不能为空", trigger: "blur"},],
});
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      if(form.watchType === '1'){
        form.projectIds = [];
      }else if(form.watchType === '2'){
        form.screenIds = [];
      }
      const response = await api.createNotice(
          {name: form.name,
                notice_type: form.noticeType.toString(),
                webhook_url: form.webhookUrl,
                at_all: form.atAll,
                remarks: form.remarks,
                watch_type: form.watchType,
                screen_ids: form.screenIds.toString(),
                project_ids: form.projectIds.toString(),
                faild_count: form.faildCount,
                timeout_count: form.timeOutCount,
          });
      if (response.data) {
        await router.push({name:'notices', query: router.currentRoute.value.query})
        ElMessage.success('添加报警群组成功！');
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