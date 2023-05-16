
export const getLastItem = (path:string) =>  { //获取url路径最后一段内容
    return path.substring(path.lastIndexOf('/') + 1)
}