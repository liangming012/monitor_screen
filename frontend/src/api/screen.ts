import http from '../utils/http/http.ts'

export const screen = {
    async getList() {
        return http.get(`screens/list`, {});
    },
    async getScreens(data) {
        return http.get(`screens/`, data);
    },
    async getScreen(screenId: string) {
        return http.get(`screens/${screenId}`, {});
    },
    async updateScreen(screenId: string, data) {
        return http.put(`screens/${screenId}`, data);
    },
    async createScreen(data) {
        return http.post(`screens/`, data);
    },
    async deleteScreen(screenId: string) {
        return http.del(`screens/${screenId}`, {});
    }
}
