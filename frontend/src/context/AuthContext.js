import { createContext, useState, useEffect } from "react";
import {
  getUserFromToken,
  clearAuth,
  setToken,
  getToken,
  isTokenExpired, // Importation de la fonction pour vérifier l'expiration du token
} from "../utils/authHelpers";
import axiosInstance from "../utils/axiosInstance";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fonction de connexion
  const login = async (email, motDePasse) => {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", motDePasse);

    const res = await axiosInstance.post("/auth/token", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    const token = res.data.access_token;
    setToken(token);

    const userData = await getUserFromToken(token);
    setUser(userData);
  };

  // Fonction de déconnexion
  const logout = () => {
    clearAuth();
    setUser(null);
  };

  // Fonction pour récupérer l'utilisateur actuel
  const fetchCurrentUser = async () => {
    try {
      const res = await axiosInstance.get("/utilisateurs/moi");
      setUser(res.data);
    } catch (err) {
      logout(); // Si une erreur se produit, on déconnecte l'utilisateur
    } finally {
      setLoading(false); // Fin du chargement
    }
  };

  // Vérifie si un token est présent et valide, et récupère les informations de l'utilisateur
  useEffect(() => {
    const token = getToken();
    if (token && !isTokenExpired(token)) { // Vérifie si le token est valide
      setToken(token); // Ajoute le token aux headers de toutes les requêtes
      fetchCurrentUser(); // Récupère les données de l'utilisateur
    } else {
      logout(); // Si le token est expiré ou inexistant, déconnecte l'utilisateur
      setLoading(false); // Fin du chargement
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
