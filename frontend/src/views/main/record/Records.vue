<template>
  <div>
    <el-card class="box-card">
      <template #header>
        <RecordHeader :list=true></RecordHeader>
      </template>
      <el-row type="flex" justify="space-between">
        <el-button type="primary" @click="router.push({name:'addRecord', query:searchForm})">添加记录</el-button>
        <div>
          <el-select style="width:20rem;" v-model="searchForm.id" @change="searchAction" placeholder="请选择要搜索的项目" clearable @clear="searchAction">
            <el-option
                v-for="project in projects"
                :key="project.id.toString()"
                :label="project.name"
                :value="project.id.toString()"
            />
          </el-select>
          <el-button icon="Search" @click="searchAction" />
        </div>
      </el-row>
      <el-row>
        <el-table stripe :data="tableData" border style="width: 100%;margin-top:2rem">
          <el-table-column prop="id" label="ID"/>
          <el-table-column prop="project.name" label="项目名称"/>
          <el-table-column prop="build_id" label="构建ID"/>
          <el-table-column prop="url" label="构建地址"/>
          <el-table-column prop="duration" label="持续时间"/>
          <el-table-column prop="check_time" label="检查时间">
            <template #default="scope">
              {{getDate(scope.row.check_time)}}
            </template>
          </el-table-column>
          <el-table-column prop="create_time" label="创建时间">
            <template #default="scope">
              {{getDate(scope.row.create_time)}}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态">
            <template #default="scope">
                <el-tag type="success" v-if="scope.row.status===0">成功</el-tag>
                <el-tag type="danger" v-else-if="scope.row.status===1">失败</el-tag>
                <el-tag type="warning" v-else-if="scope.row.status===2">超时</el-tag>
                <el-tag type="info" v-else>失效</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作"  width="140px">
            <template #default="scope">
              <el-button type="danger" size="small" @click="deleteAction(scope.row.id)">删除</el-button>
              <el-button size="small" @click="router.push({name: 'editRecord', params: {'id': scope.row.id}, query: searchForm})">编辑</el-button>
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
import {record as api} from "../../../api/record.ts";
import RecordHeader from "../../../components/record/RecordHeader.vue";
import {getDate} from "../../../utils/date/date.ts";
import {project} from "../../../api/project.ts";

// Dom 挂载之后
onMounted(() => {
  initSearchForm();
  getListAction();})
// 表格数据
let tableData = ref([]);
let projects = ref([]);
let total = ref(0);
// 搜索条件
const searchForm = reactive({
  current: 1,
  size: 10,
  id: ''
})

const initSearchForm = ()=>{
  getProjects();
  if(JSON.stringify(router.currentRoute.value.query)!=="{}"){
    if(router.currentRoute.value.query.current){
      searchForm.current = parseInt(<string>router.currentRoute.value.query.current);
    }
    if(router.currentRoute.value.query.size){
      searchForm.size = parseInt(<string>router.currentRoute.value.query.size);
    }
    if(router.currentRoute.value.query.id){
      searchForm.id = router.currentRoute.value.query.id.toString();
    }
  }
}

// 获取列表
const getProjects = async () => {
  const res = await project.getList();
  projects.value = res.data;
}

// 获取列表
const getListAction = async () => {
  const res = await api.getRecords(searchForm);
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
    const res = await api.deleteRecord(id);
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