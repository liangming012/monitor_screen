export const getDate = (timestamp: string) => {
    let date = new Date(timestamp * 1000);  // 参数需要毫秒数，所以这里将秒数乘于 1000
    let Y = date.getFullYear() + '-';
    let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
    let D = date.getDate() + ' ';
    let h = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
    let m = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
    let s = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds();
    return Y+M+D+h+m+s;
};

export const getTimestamp = (dateString: string) => { // dateString如：2014-04-23 18:55:49:123
    return new Date(dateString).getTime();
}