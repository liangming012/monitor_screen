import http from '../utils/http/http.js'

export const show = {
    async getShows(data) {
        return http.get(`shows/`, data);
    },
    async getShow(showId: string) {
        return http.get(`shows/${showId}`, {});
    },
    async updateShow(showId: string, data) {
        return http.put(`shows/${showId}`, data);
    },
    async createShow(data) {
        return http.post(`shows/`, data);
    },
    async deleteShow(showId: string) {
        return http.del(`shows/${showId}`, {});
    }
}
