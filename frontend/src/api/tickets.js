import axios from "../utils/axiosInstance";

// Liste des tickets (filtrée selon rôle côté backend)
export const getTickets = async ({ statut, priorite, sort }) => {
  const params = {};
  if (statut) params.statut = statut;
  if (priorite) params.priorite = priorite;
  if (sort) params.sort = sort;

  const res = await axios.get("/tickets", { params });
  return res.data;
};

// Créer un nouveau ticket (employé)
export const createTicket = async (data) => {
  const res = await axios.post("/tickets", data);
  return res.data;
};

// Obtenir les détails d’un ticket
export const getTicketById = async (id) => {
  const res = await axios.get(`/tickets/${id}`);
  return res.data;
};

// Modifier un ticket
export const updateTicket = async (id, updates) => {
  const res = await axios.put(`/tickets/${id}`, updates);
  return res.data;
};

// Assigner des techniciens (admin)
export const assignTechniciensToTicket = async (ticketId, technicienIds) => {
  await axios.post(`/tickets/${ticketId}/assigner`, technicienIds);
};

// Désassigner des techniciens (admin)
export const removeTechnicienFromTicket = async (ticketId, technicienId) => {
  await axios.post(`/tickets/${ticketId}/desassigner`, { technicien_id: technicienId });
};
