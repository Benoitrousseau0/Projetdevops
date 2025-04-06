import axios from "axios";
import { getToken, clearAuth } from "./authHelpers";

const axiosInstance = axios.create({
  baseURL: "http://localhost:8000", // changer par le port ou vous avez lancez fastapi sinon marche pas 
});

axiosInstance.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearAuth();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
