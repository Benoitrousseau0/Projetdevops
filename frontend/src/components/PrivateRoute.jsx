// src/components/PrivateRoute.jsx
import { Navigate } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

// PrivateRoute protège les routes qui nécessitent d'être authentifié
const PrivateRoute = ({ element, ...rest }) => {
  const { user } = useContext(AuthContext); // Vérifie si l'utilisateur est connecté

  // Si l'utilisateur est connecté, on affiche l'élément, sinon on redirige vers /login
  if (!user) {
    return <Navigate to="/login" />;
  }

  return element;
};

export default PrivateRoute;
