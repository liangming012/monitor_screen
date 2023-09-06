<template>
  <el-footer>
    <p>Copyright © 2023-2033 <el-tag @click="copy">作者邮箱：{{email}}</el-tag></p>
  </el-footer>
</template>
<script setup lang="ts">
import {ElMessage} from "element-plus";

const email = 'liangming012@gmail.com';
const copy = ()=>{
  if (navigator.clipboard) {
    // clipboard api 复制
    navigator.clipboard.writeText(email);
  } else {
    let textarea = document.createElement('textarea');
    document.body.appendChild(textarea);
    // 隐藏此输入框
    textarea.style.position = 'fixed';
    textarea.style.clip = 'rect(0 0 0 0)';
    textarea.style.top = '0px';
    // 赋值
    textarea.value = email;
    // 选中
    textarea.select();
    // 复制
    document.execCommand('copy', true);
    // 移除输入框
    document.body.removeChild(textarea);
    ElMessage.info('邮箱复制成功！');
  }
};
</script>
<style scoped>
.el-footer {
  color: #cccccc;
  text-align: center;
}

.el-footer:hover {
  color: #2661ef;
}
</style>
