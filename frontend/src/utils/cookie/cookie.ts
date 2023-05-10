
export const setCookie = (name: string, val: string, exp: number = 0, path:string = '/') => {
    let  expires = '';
    if(exp){
        const date = new Date();
        // Set it expire in 7 days
        date.setTime(date.getTime() + (exp * 24 * 60 * 60 * 1000));
        expires = date.toUTCString();
    }
    // Set it
    document.cookie = name+"="+val+"; expires="+expires+"; path=" + path;
}

export const getCookie = (name: string) => {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length == 2) {
        return parts.pop().split(";").shift();
    }
}
export const deleteCookie = (name: string, path:string = '/') => {
    const date = new Date();
    // Set it expire in -1 days
    date.setTime(date.getTime() + (-1 * 24 * 60 * 60 * 1000));
    // Set it
    document.cookie = name+"=; expires="+date.toUTCString()+"; path=" + path;
}

export const getToken = () => getCookie('token');

export const saveToken = (token: string) => setCookie('token', token);

export const removeToken = () => deleteCookie('token');