import http from '../utils/http/http.js'
import {IUserProfile, IUserProfileCreate, IUserProfileUpdate} from "../interfaces";

export const user = {
    async logInGetToken(username: string, password: string) {
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);
        params.append('grant_type', 'password');
        params.append('scope', '');
        params.append('client_id', '');
        params.append('client_secret', '');
        return http.post(`login/access-token`, params);
    },
    async getMe() {
        return http.get<IUserProfile>('users/me', {})
    },
    async updateMe(data: IUserProfileUpdate) {
        return http.put<IUserProfile>(`users/me`, data);
    },
    async getUsers() {
        return http.get<IUserProfile[]>(`users/`, {});
    },
    async updateUser(userId: number, data: IUserProfileUpdate) {
        return http.put(`users/${userId}`, data);
    },
    async createUser(data: IUserProfileCreate) {
        return http.post(`users/`, data);
    }
}
