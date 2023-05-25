
export const isEmail = (rule, value, callback) => {
    if (!/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((.[a-zA-Z0-9_-]{2,3}){1,2})$/.test(value)) {
        callback(new Error('必须是邮箱格式！'));
    } else {
        callback();
    }
}

export const isEmptyArray = (rule, value, callback) => {
    if (value && value.length<=0) {
        callback(new Error('最少选择一项！'));
    } else {
        callback();
    }
}