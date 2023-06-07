<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <UserHeader :list=true></UserHeader>
      </template>
      <el-row type="flex" justify="space-between">
        <el-button type="primary" @click="router.push({name:'addUser', query:searchForm})">添加用户</el-button>
        <el-input style="width:20rem;" @blur="searchAction" @clear="searchAction" @keyup.enter="searchAction" clearable v-model.trim="searchForm.name" placeholder="请输入用户姓名">
          <template #append>
            <el-button icon="Search" @click="searchAction" />
          </template>
        </el-input>
      </el-row>
      <el-row>
        <el-table stripe :data="tableData" border style="width: 100%;margin-top:2rem">
          <el-table-column prop="id" label="ID"/>
          <el-table-column prop="full_name" label="姓名"/>
          <el-table-column prop="email" label="邮箱"/>
          <el-table-column  prop="is_active" label="是否激活">
            <template #default="scope">
              <el-switch
                  v-model="scope.row.is_active"
                  inline-prompt
                  active-text="是"
                  inactive-text="否"
                  disabled
              />
            </template>
          </el-table-column>
          <el-table-column prop="roles" label="角色">
            <template #default="scope">
              <template v-for="role in scope.row.roles.split(',')">
                <el-tag v-show="role==='10001'">管理员</el-tag>
                <el-tag v-show="role==='10002'">普通用户</el-tag>
              </template>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="140px">
            <template #default="scope">
              <el-button type="danger" size="small" @click="deleteAction(scope.row.id)">删除</el-button>
              <el-button size="small" @click="router.push({name: 'editUser', params: {'id': scope.row.id}, query: searchForm})">编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
      <el-row type="flex" justify="center">
      <!-- 分页 -->
      <el-pagination style="margin-top:20px" background :current-page="searchForm.current" :page-size="searchForm.size"
                     :page-sizes="[10, 20, 30, 40]" layout="->,total, sizes, prev, pager, next, jumper" :total="total"
                     @size-change="handleSizeChange" @current-change="handleCurrentChange" />
      </el-row>

    </el-card>
  </div>
</template>

<script setup lang="ts">
import UserHeader from "../../../components/user/UserHeader.vue";
import {ElMessage, ElMessageBox} from "element-plus";
import {onMounted, reactive, ref} from "vue";
import {user} from "../../../api/user.ts";
import router from "../../../router/index.ts";
// Dom 挂载之后
onMounted(() => {
  initSearchForm();
  getListAction();})
// 用户数据
let tableData = ref([]);
let total = ref(0);
// 搜索条件
const searchForm = reactive({
  current: 1,
  size: 10,
  name: ''
})

const initSearchForm = ()=>{
  if(JSON.stringify(router.currentRoute.value.query)!=="{}"){
    if(router.currentRoute.value.query.current){
      searchForm.current = parseInt(<string>router.currentRoute.value.query.current);
    }
    if(router.currentRoute.value.query.size){
      searchForm.size = parseInt(<string>router.currentRoute.value.query.size);
    }
    if(router.currentRoute.value.query.name){
      searchForm.name = <string>router.currentRoute.value.query.name;
    }
  }
}
// 获取列表
const getListAction = async () => {
  const res = await user.getUsers(searchForm);
  tableData.value = res.data.records;
  total.value = res.data.total;
}
const handleSizeChange = (size) => {
  searchForm.size = size;
  getListAction();
}
const handleCurrentChange = (current) => {
  searchForm.current = current;
  getListAction();
}
const searchAction = () => {
  searchForm.current = 1;
  getListAction();
}
// 删除用户
const deleteAction = (id) => {
  ElMessageBox.confirm(
      '确定要删除吗?',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(async () => {
    const res = await user.deleteUser(id);
    if (res.data.msg) {
      ElMessage.success("删除成功")
      await getListAction();
    } else {
      ElMessage.error("删除失败")
    }
  }).catch(() => {
    ElMessage({type: 'info',message: '取消删除'})
  })
}
</script>

<style scoped>
</style>