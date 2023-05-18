<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <ScreenHeader :edit=true :return=true></ScreenHeader>
      </template>
      <el-form :model="form" :rules="rules" ref="ruleFormRef"  label-position="right" label-width="8rem">
        <el-form-item label="屏幕名称:" prop="name">
          <el-input v-model="form.name" placeholder="请输入屏幕名称" />
        </el-form-item>
        <el-form-item label="显示行数:" prop="row">
          <el-input type="number" v-model="form.row" placeholder="请输入屏幕内容显示行数" />
        </el-form-item>
        <el-form-item label="显示列数:" prop="col">
          <el-input type="number" v-model="form.col" placeholder="请输入屏幕内容显示列数" />
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
import ScreenHeader from "../../../components/screen/ScreenHeader.vue";
import {screen as api} from "../../../api/screen.ts";
const form = reactive({
  name: '',
  row: 1,
  col: 1,
});

onMounted(() => {getProject();})
const props = defineProps({id:String});
const getProject = async () => {
  const res = await api.getScreen(props.id);
  form.name = res.data.name;
  form.row = res.data.row;
  form.col = res.data.col;
}
const rules = reactive({
  name: [{ required: true, message: "屏幕名称不能为空", trigger: "blur"},
    {max:50, message: "屏幕名称不能超过50个字符"}],
  row: [{ required: true, message: "显示行数不能为空", trigger: "blur" },
    { pattern: /^[0-9]*$/, message: "显示行数必须为数字", trigger: "blur" }],
  col: [{ required: true, message: "显示列数不能为空", trigger: "blur" },
    { pattern: /^[0-9]*$/, message: "显示列数必须为数字", trigger: "blur" }],
});
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      const response = await api.updateScreen(
          props.id,
          {name: form.name,
              row: form.row,
              col: form.col,
          });
      if (response.data) {
        await router.push({name:'screens', query: router.currentRoute.value.query})
        ElMessage.success('编辑屏幕成功！');
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