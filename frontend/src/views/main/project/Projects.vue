<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <ProjectHeader :list=true></ProjectHeader>
      </template>
      <el-row type="flex" justify="space-between">
        <el-button type="primary" @click="router.push({name:'addProject', query:searchForm})">添加项目</el-button>
        <el-input style="width:20rem;" @blur="searchAction" @clear="searchAction" clearable v-model.trim="searchForm.name" placeholder="请输入项目名称">
          <template #append>
            <el-button icon="Search" @click="searchAction" />
          </template>
        </el-input>
      </el-row>
      <el-row>
        <el-table stripe :data="tableData" border style="width: 100%;margin-top:2rem">
          <el-table-column prop="id" label="ID"/>
          <el-table-column prop="name" label="项目名称"/>
          <el-table-column prop="duration_limit" label="持续时间"/>
          <el-table-column prop="jenkins_url" label="Jenkins URL"/>
          <el-table-column  prop="enable" label="是否启用">
            <template #default="scope">
              <el-switch
                  v-model="scope.row.enable"
                  inline-prompt
                  active-text="是"
                  inactive-text="否"
                  disabled
              />
            </template>
          </el-table-column>
          <el-table-column label="操作"  width="140px">
            <template #default="scope">
              <el-button type="danger" size="small" @click="deleteAction(scope.row.id)">删除</el-button>
              <el-button size="small" @click="router.push({name: 'editProject', params: {'id': scope.row.id}, query: searchForm})">编辑</el-button>
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
import {ElMessage, ElMessageBox} from "element-plus";
import {onMounted, reactive, ref} from "vue";
import router from "../../../router/index.ts";
import ProjectHeader from "../../../components/project/ProjectHeader.vue";
import {project as api} from "../../../api/project.ts";
// Dom 挂载之后
onMounted(() => {
  initSearchForm();
  getListAction();})
// 表格数据
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
  const res = await api.getProjects(searchForm);
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
// 删除
const deleteAction = (id) => {
  ElMessageBox.confirm(
      '确定要删除吗?',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(async () => {
    const res = await api.deleteProject(id);
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