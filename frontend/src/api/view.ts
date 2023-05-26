import http from '../utils/http/http.js'
import {IUserProfile} from "../interfaces";

export const view = {
    async getViewData(screenId:string) {
        return http.get(`screens/${screenId}/show`, {})
    }
}
