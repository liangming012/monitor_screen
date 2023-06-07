
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

export const minNumber = (rule, value, callback) => {
    if(typeof rule.min === 'number' && rule.min%1 === 0){
        if (value && value < rule.min) {
            callback(new Error('必须大于等于 ' + rule.min));
        } else {
            callback();
        }
    }else {
        callback(new Error('必须有min参数，且值必须是数字'));
    }
}

export const maxNumber = (rule, value, callback) => {
    if(typeof rule.max === 'number' && rule.max%1 === 0){
        if (value && value >= rule.max) {
            callback(new Error('必须小于等于 ' + rule.max));
        } else {
            callback();
        }
    }else {
        callback(new Error('必须有max参数，且值必须是数字'));
    }
}