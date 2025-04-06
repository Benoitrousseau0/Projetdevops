import axios from "../utils/axiosInstance";

// Obtenir toutes les notifications de l'utilisateur
export const getNotifications = async () => {
  const res = await axios.get("/notifications");
  return res.data;
};

// Marquer une notification comme lue
export const markAsRead = async (notifId) => {
  const res = await axios.post(`/notifications/${notifId}/lu`);
  return res.data;
};

// Marquer toutes les notifications comme lues
export const markAllAsRead = async () => {
  const res = await axios.post("/notifications/lu-toutes");
  return res.data;
};
