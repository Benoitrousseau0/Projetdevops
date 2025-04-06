import axios from "../utils/axiosInstance";

// Obtenir tous les utilisateurs (admin uniquement)
export const getUtilisateurs = async () => {
  const res = await axios.get("/utilisateurs");
  return res.data;
};

// Supprimer un utilisateur (admin)
export const deleteUtilisateur = async (id) => {
  const res = await axios.delete(`/utilisateurs/${id}`);
  return res.data;
};

// Modifier son profil (nom + email)
export const updateProfil = async ({ nom, email }) => {
  const res = await axios.put("/utilisateurs/moi", { nom, email });
  return res.data;
};

// Changer son mot de passe
export const changePassword = async ({ ancien_mot_de_passe, nouveau_mot_de_passe }) => {
  const res = await axios.put("/utilisateurs/password", {
    ancien_mot_de_passe,
    nouveau_mot_de_passe,
  });
  return res.data;
};

// Assigner des techniciens à un ticket (appelé dans AssignTechnicians)
export const assignTechniciens = async (ticketId, technicien_ids) => {
  const res = await axios.post(`/tickets/${ticketId}/assigner`, technicien_ids);
  return res.data;
};

// Désassigner un technicien d'un ticket
export const removeTechnicien = async (ticketId, technicien_id) => {
  const res = await axios.post(`/tickets/${ticketId}/desassigner`, { technicien_id });
  return res.data;
};

// Inscription d'un nouvel utilisateur (rôle employé par défaut)
export const registerUtilisateur = async ({ nom, email, mot_de_passe }) => {
  const res = await axios.post("/utilisateurs", {
    nom,
    email,
    mot_de_passe,
  });
  return res.data;
};

export const updateUtilisateurRole = async (userId, newRole) => {
  const token = localStorage.getItem('access_token'); // Récupère le jeton depuis le stockage local ou le contexte

  const response = await fetch(`http://localhost:8000/admin/utilisateurs/${userId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`, // Ajoute le jeton ici
    },
    body: JSON.stringify({ new_role: newRole }),
  });

  if (!response.ok) {
    throw new Error('Erreur lors de la mise à jour du rôle');
  }

  return response.json();
};
