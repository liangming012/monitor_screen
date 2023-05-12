import http from '../utils/http/http.js'
import {IProjectProfile} from "../interfaces";

export const Project = {
    async getProjects(data) {
        return http.get(`projects/`, data);
    },
    async getProject(projectId: string) {
        return http.get(`projects/${projectId}`, {});
    },
    async updateProject(projectId: string, data) {
        return http.put(`projects/${projectId}`, data);
    },
    async createProject(data) {
        return http.post(`projects/`, data);
    },
    async deleteProject(projectId: string) {
        return http.del(`projects/${projectId}`, {});
    }
}
