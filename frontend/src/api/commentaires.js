import axios from "../utils/axiosInstance";

// Récupérer les commentaires liés à un ticket
export const getCommentairesByTicket = async (ticketId) => {
  const res = await axios.get(`/commentaires/ticket/${ticketId}`);
  return res.data;
};

// Ajouter un commentaire à un ticket
export const addCommentaire = async (ticketId, contenu) => {
  const res = await axios.post("/commentaires", {
    id_ticket: ticketId,  // Assure-toi que ticketId est bien passé ici
    contenu,
  });
  return res.data;
};

// Mettre à jour un commentaire
export const updateCommentaire = async (ticketId, commentaireId, contenu) => {
  const res = await axios.put(`/commentaires/ticket/${ticketId}/commentaires/${commentaireId}`, {
    contenu,
  });
  return res.data;
};

// Supprimer un commentaire
export const deleteCommentaire = async (ticketId, commentaireId) => {
  const res = await axios.delete(`/commentaires/ticket/${ticketId}/commentaires/${commentaireId}`);
  return res.data;
};
