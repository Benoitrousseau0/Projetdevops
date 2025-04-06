import axiosInstance from "../utils/axiosInstance";

// Fonction pour récupérer les statistiques du tableau de bord
export const getDashboardStats = async () => {
  const res = await axiosInstance.get("/admin/dashboard");
  return res.data;
};