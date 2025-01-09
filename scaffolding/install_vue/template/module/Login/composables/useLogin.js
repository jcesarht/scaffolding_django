import {%module_name%Service } from "../services/%module_name%Service"; 

export async function use%module_name%(usernameParam, passwordParam){
    const username = usernameParam
    const password = passwordParam
    let loading = false;
    let error = false;
    let response = null

    const fetchLogin = async () => {
        try {
            if (username && username == ''){
                throw Error("Please check the param username")
            }
            loading = true;
            const res = await %module_name%Service.getAuth(username, password)
            response = {
                data: res.data.data.data,
                error: res.error,
                message: res.data.data.message
            }
        } catch (err) {
            error = true;
            response = {
                error: true,
                message: err.message
            }
        } finally {
            loading = false;
        }
    };
    
    await fetchLogin();
    
    return { response, error, loading ,fetchLogin };
}

export async function useSignin(userDataParam){
    let error = false;
    let response = null
    let loading = false
    const userData = userDataParam
    const fetchSignin = async ()=>{
        try {
            if (userData == {}){
                throw Error("Please check the param username")
            }
            loading = true;
            const res = await %module_name%Service.signin(userData)
            response = {
                data: res.data.data.data,
                error: res.error,
                message: res.data.data.message
            }
        } catch (err) {
            error = true;
            response = {
                error: true,
                message: err.message
            }
        } finally {
            loading = false;
        }
    }

    await fetchSignin()

    return {error, response, loading}
}
