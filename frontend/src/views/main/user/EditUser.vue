<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <UserHeader :edit=true :return=true></UserHeader>
      </template>
      <el-form :model="form" :rules="rules" ref="ruleFormRef"  label-position="right" label-width="8rem">
        <el-form-item label="姓名:" prop="fullName">
          <el-input v-model="form.fullName" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱:" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="密码:" prop="password">
          <el-input type="password" v-model="form.password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="是否激活:" prop="isActive">
          <el-switch v-model="form.isActive"/>
        </el-form-item>
        <el-form-item label="权限角色:" prop="roles">
          <el-checkbox-group v-model="form.roles">
            <el-checkbox label="管理员"/>
            <el-checkbox label="普通用户" checked />
          </el-checkbox-group>
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
import UserHeader from "../../../components/user/UserHeader.vue";
import {onMounted, reactive, ref} from "vue";
import {user as api} from "../../../api/user.ts";
import {ElMessage} from "element-plus";
import router from "../../../router/index.ts";
const form = reactive({
  fullName: '',
  email: '',
  password: '',
  isActive: true,
  roles: [],
});

onMounted(() => {getUserList();})
const props = defineProps({id:String});
const getUserList = async () => {
  const res = await api.getUser(props.id);
  form.fullName = res.data.full_name;
  form.email = res.data.email;
  form.isActive = res.data.is_active;
  let roles = []
  const splitData = res.data.roles.split(',');
  for(let role in splitData){
    if(splitData[role] === '10001'){
      roles.push('管理员');
    }
    if(splitData[role] === '10002'){
      roles.push('普通用户');
    }
  }
  form.roles = roles;
}

const rules = reactive({
  fullName: [{ required: true, message: "姓名不能为空", trigger: "blur"},
    {max:50, message: "姓名不能超过50个字符"}],
  email: [{ required: true, message: "邮箱不能为空", trigger: "blur" },
    {type: 'email', message: "必须是邮箱格式", trigger: "blur"}],
  password: [{max:50, message: "密码不能超过50个字符"}],
  roles: [{ required: true, type: 'array', message: "角色不能为空", trigger: "change"}],
});
const ruleFormRef = ref();
const onSubmit = () => {
  if (!ruleFormRef) return;
  ruleFormRef.value.validate(async (valid) => {
    if (valid) {  // 表单验证通过
      const response = await api.updateUser(
          props.id,
          {full_name: form.fullName,
                email: form.email,
                password: form.password,
                is_active: form.isActive,
                roles: form.roles.toString().replace('管理员', '10001').replace('普通用户', '10002'),
          });
      if (response.data) {
        await router.push({name:'users', query: router.currentRoute.value.query})
        ElMessage.success('编辑用户成功！');
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