import http from '../utils/http/http.ts'

export const record = {
    async getRecords(data) {
        return http.get(`records/`, data);
    },
    async getRecord(recordId: string) {
        return http.get(`records/${recordId}`, {});
    },
    async updateRecord(recordId: string, data) {
        return http.put(`records/${recordId}`, data);
    },
    async createRecord(data) {
        return http.post(`records/`, data);
    },
    async deleteRecord(recordId: string) {
        return http.del(`records/${recordId}`, {});
    }
}
