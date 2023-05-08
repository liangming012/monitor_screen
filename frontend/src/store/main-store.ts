import { defineStore } from 'pinia'
import {MainState} from "../interfaces/index";
import {user} from "../api/user";
import {getLocalToken, removeLocalToken, saveLocalToken} from "../utils/storage/localStorage";
import router from "../router";
import {AxiosError} from "axios";
import {ElMessage} from "element-plus";


export const useMainStore = defineStore('main', {
  // 其他配置...
  state:():MainState =>({
    isLoggedIn: null,
    token: '',
    logInError: false,
    userProfile: null,
    dashboardMiniDrawer: false,
    dashboardShowDrawer: true,
    notifications: [],
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
        const token = response.data.access_token;
        if (token) {
          saveLocalToken(token);
          this.token = token;
          this.isLoggedIn = true;
          this.logInError = false;
          await this.actionGetUserProfile();
          if (router.currentRoute.value.path === '/login' || router.currentRoute.value.path === '/') {
            await router.push('/main');
          }
          ElMessage.success('登录成功！');
        } else {
          await this.actionLogOut();
        }
      } catch (err) {
        this.logInError = true;
        await this.actionLogOut();
      }
    },
    async actionGetUserProfile() {
      try {
        const response = await user.getMe(this.token);
        if (response.data) {
          this.userProfile = response.data;
        }
      } catch (error) {
        await this.actionCheckApiError(error);
      }
    },
    async actionUpdateUserProfile(payload) {
      try {
        const loadingNotification = { content: 'saving', showProgress: true };
        this.notifications.push(loadingNotification);
        const response = (await Promise.all([
          user.updateMe(this.token, payload),
          await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
        ]))[0];
        this.userProfile = response.data;
        this.notifications = this.notifications.filter((notification) => notification !== loadingNotification);
        this.notifications.push({ content: 'Profile successfully updated', color: 'success' });
      } catch (error) {
        await this.actionCheckApiError(error);
      }
    },
    async actionCheckLoggedIn() {
      if (!this.isLoggedIn) {
        let token = this.token;
        if (!token) {
          const localToken = getLocalToken();
          if (localToken) {
            this.token = localToken;
            token = localToken;
          }
        }
        if (token) {
          try {
            const response = await user.getMe(token);
            this.isLoggedIn = true;
            this.userProfile = response.data;
          } catch (error) {
            await this.actionRemoveLogIn();
          }
        } else {
          await this.actionRemoveLogIn();
        }
      }
    },
    async actionLogOut() {
      sessionStorage.clear();
      removeLocalToken();
      this.token = '';
      this.isLoggedIn = false;
      if (router.currentRoute.path !== '/login') {
        router.push('/login');
      }
    },
    async actionUserLogOut() {
      await this.actionLogOut();
      this.notifications.push({ content: 'Logged out', color: 'success' });
    },
    async actionCheckApiError(payload: AxiosError) {
      if (payload.response!.status === 401) {
        await this.actionLogOut();
      }
    },
  },
})
