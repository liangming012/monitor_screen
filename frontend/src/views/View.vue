<template>
  <div id="main">
    <div v-if="networkError" class="network_error">网络错误！</div>
    <div v-for="record in records">
      <div v-if="record.status === 0">
        <a id="a_link" :href="record.url" target="_blank">
          <div class="project">
            <div class="success">
              <div class="name"><strong>{{ record.name }}</strong></div>
              <div class="time">检查时间:{{ getDateTime(record.check_time) }}</div>
            </div>
          </div>
        </a>
      </div>
      <div v-if="record.status === 1">
        <a id="a_link" :href="record.url" target="_blank">
          <div class="project">
            <div class="error">
              <div class="name"><strong>{{ record.name }}</strong></div>
              <div class="time">检查时间:{{ getDateTime(record.check_time) }}</div>
            </div>
          </div>
        </a>
      </div>
      <div v-if="record.status === 2">
        <a id="a_link" :href="record.url" target="_blank">
          <div class="project">
            <div class="warning">
              <div class="name"><strong>{{ record.name }}</strong></div>
              <div class="time">检查时间:{{ getDateTime(record.check_time) }}</div>
            </div>
          </div>
        </a>
      </div>
      <div v-if="record.status === 999">
        <a id="a_link" :href="record.url" target="_blank">
          <div class="project">
            <div class="invalid">
              <div class="name"><strong>{{ record.name }}</strong></div>
              <div class="time">检查时间:{{ getDateTime(record.check_time) }}</div>
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from "vue";
import router from "../router/index.ts";
import {getLastItem} from "../utils/common";
import {getDateTime} from "../utils/date/date.ts";
import axios from "axios";

let row = ref(1);
let col = ref(1);
let networkError = ref(false);
const records = ref([]);
onMounted(() => {
  setInterval(getViewData, 3000)
});
const instance = axios.create({
  // 接口
  baseURL: import.meta.env.VITE_APP_DOMAIN + "/api/v1/",
  // 超时时间
  timeout: 30000,
});

const getViewData = async () => {
  instance.get(`screens/${getLastItem(router.currentRoute.value.path)}/show`)
      .then(function (response) {
        // handle success
        row.value = response.data.screen.row;
        col.value = response.data.screen.col;
        records.value = response.data.data;
        networkError.value = false;
      })
      .catch(function (error) {
        // handle error
        console.log(error);
        if(error.code == "ERR_NETWORK"){
          networkError.value = true;
          row.value = 0;
          col.value = 0;
          records.value = [];
        }
      })
      .finally(function () {
        // always executed
      });
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

.project {
  box-sizing: border-box;
  border: 2vh solid black; /* 黑色间距*/
  padding: 1vh; /* 白色边框*/
  background-color: white;
  width: v-bind(100/col+ "vw"); /* 动态计算每个格子的宽度*/
  height: v-bind(100/row+ "vh"); /* 动态计算每个格子的高度*/
  color: white;
}

.name {
  padding-top: v-bind(20/row+ "vh"); /* 动态计算每个格子的高度*/
  /*line-height: v-bind(50/row + "vh");  !* 动态计算每个格子的高度*!*/
  /*height: v-bind(50/row + "vh");  !* 动态计算每个格子的高度*!*/
  font-size: calc(4vw); /* calc函数动态计算相对窗口宽度大小 */
}

.time {
  /*line-height: v-bind(40/row + "vh");  !* 动态计算每个格子的高度*!*/
  /*height: v-bind(40/row + "vh");  !* 动态计算每个格子的高度*!*/
  font-size: calc(2vw);
}

.success {
  height: 100%;
  background-color: green;
}

.error {
  height: 100%;
  background-color: red;
}

.warning {
  height: 100%;
  background-color: orange;
}

.invalid {
  height: 100%;
  background-color: darkgray;
}

#a_link {
  text-decoration: none;
  color: white;
}

.network_error {
  height: 80vh;
  line-height: 80vh;
  width: 80vw;
  font-size: calc(10vw);
  background-color: red;
}
</style>
