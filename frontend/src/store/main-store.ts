import { defineStore } from 'pinia'
import {MainState} from "../interfaces/index";
import {user} from "../api/user";
import router from "../router";
import {AxiosError} from "axios";
import {ElMessage} from "element-plus";
import {getToken, removeToken, saveToken} from "../utils/cookie/cookie";


export const useMainStore = defineStore('main', {
  // 其他配置...
  state:():MainState =>({
    token: '',
    userProfile: null,
  }),
  getters: {
    hasAdminAccess: (state: MainState) => {
      return (state.userProfile && state.userProfile.is_active && (state.userProfile.roles.split(',').indexOf('10001') > -1));
    }
  },
  actions: {
    async actionLogIn(payload: { username: string; password: string }) {
      try {
        const response = await user.logInGetToken(payload.username, payload.password);
        this.token = response.data.access_token;
        if (this.token) {
          saveToken(this.token);
          await this.actionGetUserProfile();
          await router.push('/main');
          ElMessage.success('登录成功！');
        } else {
          await this.clearData();
          ElMessage.error(response.data.detail);
        }
      } catch (err) {
        await this.clearData();
      }
    },
    async actionGetUserProfile() {
      try {
        const response = await user.getMe();
        if (response.data) {
          this.userProfile = response.data;
        }
      } catch (error) {
        await this.actionCheckApiError(error);
      }
    },
    async actionUpdateUserProfile(payload) {
      try {
        const response = await user.updateMe(payload);
        if (response.data) {
          this.userProfile = response.data;
          ElMessage.success('用户密码修改成功！');
        }
      } catch (error) {
        await this.actionCheckApiError(error);
      }
    },
    async actionCheckLoggedIn() {
      this.token = getToken();
      if(this.token){
        if(!this.userProfile){
          await this.actionGetUserProfile()
        }
      }else{
        await this.clearData();
      }
    },
    async clearData() {
      sessionStorage.clear(); // 清楚菜单链接路径等内容
      removeToken();
      this.token = '';
      if(router.currentRoute.value.name !== 'login'){
        await router.push('/login');
      }
    },
    async actionLogOut() {
      await this.clearData();
      ElMessage.success('退出系统！');
    },
    async actionCheckApiError(payload: AxiosError) {
      if (payload.response!.status === 401) {
        await this.actionLogOut();
      }
    },
  },
})
