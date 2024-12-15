import axios from "axios";

const axiosInstance = axios.create({
    'baseURL': 'http://127.0.0.1:8000',
    'headers':{
        'Content-Type': 'application/json',
    },
})

axiosInstance.interceptors.response.use(
    response => response,
    error => {
        const error_response = {
            error: true,
            message:""
        }
        if (!error.response) {
            if (error.code === 'ERR_NETWORK') {
                error_response.message = "We have lost the connection. Try again in a few minutes."
            }else if (error.code === 'ECONNABORTED') {
                error_response.message = "The request has taken too long. The response was rejected."
            }else if (error.code === 'ERR_BAD_REQUEST'){
                error_response.message = "Something was wrong with the request. Please check the information and try again"
            }else if(error.code === 'ERR_BAD_RESPONSE'){
                error_response.message = "Something was wrong with the service. We are fixing it as soon as possible"
            }else if (error.code === "ERR_CANCELED"){
                error_response.message = "The request has been canceled"
            }else{
                error_response.message = "Something went wrong. Try again in a moment or contact to support."
            }

        }else{
            error_response.message = error.response.data.message
        }

        return Promise.reject(error_response)
    }
)
export default axiosInstance