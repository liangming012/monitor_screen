<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <ScreenHeader :list=true></ScreenHeader>
      </template>
      <el-row type="flex" justify="space-between">
        <el-button type="primary" @click="router.push({name:'addScreen', query:searchForm})">添加屏幕</el-button>
        <el-input style="width:20rem;" @blur="searchAction" @clear="searchAction" clearable v-model.trim="searchForm.name" placeholder="请输入屏幕名称">
          <template #append>
            <el-button icon="Search" @click="searchAction" />
          </template>
        </el-input>
      </el-row>
      <el-row>
        <el-table stripe :data="tableData" border style="width: 100%;margin-top:2rem">
          <el-table-column prop="id" label="ID"/>
          <el-table-column prop="name" label="屏幕名称"/>
          <el-table-column prop="row" label="显示行数"/>
          <el-table-column prop="col" label="显示列数"/>
          <el-table-column prop="faild_count" scoped-slot>
            <template #header>
              失败报警阈值(次)
              <el-tooltip content="连续失败超过阈值次数屏幕才会显示提示" placement="top">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="timeout_count">
            <template #header>
              超时报警阈值(次)
              <el-tooltip content="连续超时超过阈值次数屏幕才会显示提示" placement="top">
                <el-icon><QuestionFilled /></el-icon>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="操作"  width="200px">
            <template #default="scope">
              <el-button size="small" @click="openPreview(scope.row.id)">预览</el-button>
              <el-button type="danger" size="small" @click="deleteAction(scope.row.id)">删除</el-button>
              <el-button size="small" @click="router.push({name: 'editScreen', params: {'id': scope.row.id}, query: searchForm})">编辑</el-button>
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
import ScreenHeader from "../../../components/screen/ScreenHeader.vue";
import {screen as api} from "../../../api/screen.ts";
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
      searchForm.current = parseInt(router.currentRoute.value.query.current);
    }
    if(router.currentRoute.value.query.size){
      searchForm.size = parseInt(router.currentRoute.value.query.size);
    }
    if(router.currentRoute.value.query.name){
      searchForm.name = router.currentRoute.value.query.name;
    }
  }
}
// 获取列表
const getListAction = async () => {
  const res = await api.getScreens(searchForm);
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
    const res = await api.deleteScreen(id);
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
const openPreview = (id) => {
  const routeData = router.resolve({name: 'view',params: {'id': id}, query: {}});
  window.open(routeData.href, '_blank');
}
</script>

<style scoped>
</style>