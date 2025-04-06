import axiosInstance from "./axiosInstance";
import { jwtDecode } from "jwt-decode";

const TOKEN_KEY = "access_token";

// Fonction pour vérifier si le token est expiré
export const isTokenExpired = (token) => {
  const decodedToken = jwtDecode(token);  // Utilisation de jwtDecode
  const currentTime = Date.now() / 1000; // Temps actuel en secondes
  return decodedToken.exp < currentTime;  // Vérification de l'expiration
};

export const setToken = (token) => {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
    axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete axiosInstance.defaults.headers.common["Authorization"];
  }
};

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export const clearAuth = () => {
  localStorage.removeItem(TOKEN_KEY);
  delete axiosInstance.defaults.headers.common["Authorization"];
};

export const getUserFromToken = async (token) => {
  if (isTokenExpired(token)) {
    clearAuth();
    return null; // Le token a expiré, déconnecte l'utilisateur
  }
  const res = await axiosInstance.get("/utilisateurs/moi");
  return res.data;
};
