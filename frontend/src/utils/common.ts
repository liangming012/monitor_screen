
export const getLastItem = (path:string) =>  {
    return path.substring(path.lastIndexOf('/') + 1)
}