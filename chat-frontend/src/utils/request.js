import axios from 'axios'

const request = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 10000,
})

request.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API错误:', error)
    return Promise.reject(error)
  }
)

export default request
