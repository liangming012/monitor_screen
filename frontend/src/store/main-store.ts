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
    isLoading: false,
    activeMenu: '',
  }),
  getters: {
    hasAdminAccess: (state: MainState) => {
      return (state.userProfile && state.userProfile.is_active && (state.userProfile.roles.split(',').indexOf('10001') > -1));
    },
    menuData: () => {
      const store = useMainStore();
      if(store.hasAdminAccess){
        return [{"id":'1' , "name": "首页", "icon": "House", "index": "/main/dashboard", "children":[]},
          {"id":'2' , "name": "用户管理", "icon": "User", "index": "/main/user/list", "children":[]},
          {"id":'3' , "name": "项目管理", "icon": "Operation", "index": "/main/project", "children":[
              {"id": "3-1", "name": "项目列表", "icon": "", "index": "/main/project/list"},
              {"id": "3-2", "name": "记录列表", "icon": "", "index": "/main/record/list"},
            ]},
          {"id":'4' , "name": "屏幕管理", "icon": "Monitor", "index": "/main/screen", "children":[
              {"id": "4-1", "name": "屏幕列表", "icon": "", "index": "/main/screen/list"},
              {"id": "4-2", "name": "显示列表", "icon": "", "index": "/main/show/list"},
            ]},
          {"id":'5' , "name": "报警管理", "icon": "Notification", "index": "/main/notice", "children":[
              {"id": "4-1", "name": "报警群组", "icon": "", "index": "/main/notice/list"},
            ]}]
      }else {
        return [{"id":'1' , "name": "首页", "icon": "House", "index": "/main/dashboard", "children":[]},
          {"id":'3' , "name": "项目管理", "icon": "Operation", "index": "/main/project", "children":[
              {"id": "3-1", "name": "项目列表", "icon": "", "index": "/main/project/list"},
              {"id": "3-2", "name": "记录列表", "icon": "", "index": "/main/record/list"},
            ]},
          {"id":'4' , "name": "屏幕管理", "icon": "Monitor", "index": "/main/screen", "children":[
              {"id": "4-1", "name": "屏幕列表", "icon": "", "index": "/main/screen/list"},
              {"id": "4-2", "name": "显示列表", "icon": "", "index": "/main/show/list"},
            ]},
          {"id":'5' , "name": "报警管理", "icon": "Notification", "index": "/main/notice", "children":[
              {"id": "4-1", "name": "报警群组", "icon": "", "index": "/main/notice/list"},
            ]}]
      }
    },
  },
  actions: {
    changeActiveMenu(currentRoute){
      for(let mainMenu in this.menuData){
        if(currentRoute === this.menuData[mainMenu].index){
          this.activeMenu = currentRoute;
          break;
        }else {
          for(let childMenu in this.menuData[mainMenu].children){
            if(currentRoute === this.menuData[mainMenu].children[childMenu].index){
              this.activeMenu = this.menuData[mainMenu].children[childMenu].index;
              break;
            }
          }
        }
      }
    },
    actionShowLoading() {
      this.isLoading = true;
    },
    actionHideLoading() {
      this.isLoading = false;
    },
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
