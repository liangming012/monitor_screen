import instance from "./axios"

const post = (url:string, data:any): any => {
    return new Promise((resolve, reject) => {
        instance.post(url, data).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}
const get = (url:string,  data:any): any => {
    return new Promise((resolve, reject) => {
        instance.get(url, {params: data}).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}
const put = (url:string, data:any): any => {
    return new Promise((resolve, reject) => {
        instance.put(url, data).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}
const del = (url:string, data:any): any => {
    return new Promise((resolve, reject) => {
        instance.delete(url, {params: data}).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}

export default {post, get, put, del}