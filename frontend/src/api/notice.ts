import http from '../utils/http/http.ts'

export const notice = {
    async getList() {
        return http.get(`notices/list`, {});
    },
    async getNotices(data) {
        return http.get(`notices/`, data);
    },
    async getNotice(noticeId: string) {
        return http.get(`notices/${noticeId}`, {});
    },
    async updateNotice(noticeId: string, data) {
        return http.put(`notices/${noticeId}`, data);
    },
    async createNotice(data) {
        return http.post(`notices/`, data);
    },
    async deleteNotice(noticeId: string) {
        return http.del(`notices/${noticeId}`, {});
    }
}
