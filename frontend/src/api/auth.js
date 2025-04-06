import axios from "../utils/axiosInstance";

// Connexion utilisateur
export const login = async ({ email, motDePasse }) => {
  const res = await axios.post("/auth/token", {
    username: email,
    password: motDePasse,
  });
  return res.data;
};
