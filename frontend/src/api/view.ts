import http from '../utils/http/http.js'
import {IUserProfile} from "../interfaces";

export const view = {
    async getViewData(screenId) {
        return http.get('screens/${screenId}/show', {})
    }
}
