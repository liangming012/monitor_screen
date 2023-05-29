<template>
  <!--  <div id="main" class="center-in-center">-->
  <!--    <el-row justify="space-between" :gutter="10" v-for="i in row">-->
  <!--      <el-col :span="24/col" v-for="j in col">-->
  <!--        <a id="a_link" href="{{ record.url }}" target="_blank">-->
  <!--          <div class="card success">-->
  <!--            <div class="name"><strong>{{ data[j-1 + (i-1)*col ]}}</strong></div>-->
  <!--            <div class="time">检查时间：</div>-->
  <!--          </div>-->
  <!--        </a>-->
  <!--      </el-col>-->
  <!--    </el-row>-->
  <!--  </div>-->

<!--  <div v-for="d in data">-->
<!--    {{d.name}}-->
<!--  </div>-->

<!--    <div v-for="(project, index) in data">-->
<!--      {{project}}-->
<!--      {{index}}-->
<!--    </div>-->
  <div id="full">
    <div id="main" class="center-in-center">
      <div v-for="record in records">
        <div v-if="record.status === 0">
          <a id="a_link" href="{{ record.url }}" target="_blank">
            <div class="card success">
              1
<!--              <div class="name"><strong>{{ record.name }}</strong></div>-->
<!--              <div class="time">检查时间：{{ record.check_time }}</div>-->
            </div>
          </a>
        </div>
        <div v-if="record.status === 1">
          <a id="a_link" href="{{ record.url }}" target="_blank">
            <div class="card error">
              1
<!--              <div class="name"><strong>{{ record.name }}</strong></div>-->
<!--              <div class="time">检查时间：{{ record.check_time }}</div>-->
            </div>
          </a>
        </div>
        <div v-if="record.status === 2">
          <a id="a_link" href="{{ record.url }}" target="_blank">
            <div class="card warning">
              1
<!--              <div class="name"><strong>{{ record.name }}</strong></div>-->
<!--              <div class="time">检查时间：{{ record.check_time }}</div>-->
            </div>
          </a>
        </div>
        <div v-if="record.status === 999">
          <a id="a_link" href="{{ record.url }}" target="_blank">
            <div class="card invalid">
              1
<!--              <div class="name"><strong>{{ record.name }}</strong></div>-->
<!--              <div class="time">检查时间：{{ record.check_time }}</div>-->
            </div>
          </a>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup lang="ts">
import {view} from "../api/view.ts";
import {onMounted, reactive, ref} from "vue";
import router from "../router/index.ts";
import {getLastItem} from "../utils/common";

let row = ref(1);
let col = ref(1);
const records = ref([]);
// const data = reactive({arr: []});
onMounted(() => {
  getViewData();
});
const getViewData = async () => {
  const res = await view.getViewData(getLastItem(router.currentRoute.value.path));
  console.log(res.data.screen);
  console.log(res.data.data);
  row.value = res.data.screen.row;
  col.value = res.data.screen.col;
  records.value = res.data.data;
}
</script>

<style scoped>
body {
  clear: both;
  margin: 0;
  width: 100%;
  height: 100%;
  background-color: black;
}

#main {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: stretch;
  justify-content: space-between;
  align-content: stretch;
}

.card {
  width: 33.33%;
}

.name {

}

.time {

}

.success {
  background-color: green;
}

.error {
  background-color: red;
}

.warning {
  background-color: orange;
}

.invalid {
  background-color: darkgray;
}

#a_link {
  /*text-decoration: none;*/
  /*color: white;*/
}
</style>
