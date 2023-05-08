import { defineStore } from 'pinia'
import {AdminState, IUserProfile, IUserProfileCreate, IUserProfileUpdate} from "../interfaces/index";
import {api} from "../api";
export const useAdminStore = defineStore('admin', {
  // 其他配置...
  state:():AdminState => {return { users : [] }},
  getters: {
    adminUsers: (state: AdminState) => state.users,
    adminOneUser: (state: AdminState) => (userId: number) => {
      const filteredUsers = state.users.filter((user) => user.id === userId);
      if (filteredUsers.length > 0) {
        return { ...filteredUsers[0] };
      }
    },
  },
  actions: {
    async actionGetUsers() {
      const main = useMainStore();
      try {
        const response = await api.getUsers(main.token);
        if (response) {
          this.users = response.data;
        }
      } catch (error) {
        await main.actionCheckApiError(error);
      }
    },
    async actionUpdateUser(payload: { id: number, user: IUserProfileUpdate }) {
      const main = useMainStore();
      try {
        const loadingNotification = { content: 'saving', showProgress: true };
        this.notifications.push(loadingNotification);
        const response = (await Promise.all([
          api.updateUser(main.token, payload.id, payload.user),
          await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
        ]))[0];
        const users = this.users.filter((user: IUserProfile) => user.id !== response.data.id);
        users.push(payload);
        this.users = users;
        this.notifications = this.notifications.filter((notification) => notification !== loadingNotification);
        this.notifications.push({ content: 'User successfully updated', color: 'success' });
      } catch (error) {
        await main.actionCheckApiError(error);
      }
    },
    async actionCreateUser(payload: IUserProfileCreate) {
      const main = useMainStore();
      try {
        const loadingNotification = { content: 'saving', showProgress: true };
        this.notifications.push(loadingNotification);
        const response = (await Promise.all([
          api.createUser(main.token, payload),
          await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
        ]))[0];
        const users = this.users.filter((user: IUserProfile) => user.id !== response.data.id);
        users.push(payload);
        this.users = users;
        this.notifications = this.notifications.filter((notification) => notification !== loadingNotification);
        this.notifications.push({ content: 'User successfully created', color: 'success' });
      } catch (error) {
        await main.actionCheckApiError(error);
      }
    },
  },
})