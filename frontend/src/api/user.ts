import http from '../utils/http/http.js'
import {IUserProfile} from "../interfaces";

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
    async updateMe(data) {
        return http.put<IUserProfile>(`users/me`, data);
    },
    async getUsers(data) {
        return http.get<IUserProfile[]>(`users/`, data);
    },
    async updateUser(userId: number, data) {
        return http.put(`users/${userId}`, data);
    },
    async createUser(data) {
        return http.post(`users/`, data);
    }
    ,
    async deleteUser(userId: number) {
        return http.post(`users/${userId}` );
    }
}
