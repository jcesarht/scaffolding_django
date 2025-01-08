import axiosInstance from "@/services/axios.config"

export const %module_name%Service = {
    async getAuth(userParam, passwordParam) {
        const fields = {
            username: userParam,
            password: passwordParam
        }
        const response={
            error:false, 
            data:{
                http_code: 500,
                data:null
            }
        }

        const loginURL = 'api/v1/%module_name%/'
        response.data.data = await axiosInstance.post(loginURL,fields)
        response.data.http_code = response.data.data.status
        response.data.data = response.data.data.data
        
        return response
    },

    async signin (dataUser){
        const response={
            error:false, 
            data:{
                http_code: 500,
                data:null
            }
        }
        
        const fields = {
            first_name : dataUser.first_name,
            last_name : dataUser.last_name,
            username : dataUser.username,
            email : dataUser.email,
            password : dataUser.password,
        }

        const loginURL = 'api/v1/%module_name%/register/'
        response.data.data = await axiosInstance.post(loginURL,fields)
        response.data.http_code = response.data.data.status
        response.data.data = response.data.data.data

        return response
    }
}