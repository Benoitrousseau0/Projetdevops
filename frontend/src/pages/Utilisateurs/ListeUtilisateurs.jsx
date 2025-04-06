import { useEffect, useState } from "react";
import {
  getUtilisateurs,
  deleteUtilisateur,
  updateUtilisateurRole,
} from "../../api/utilisateurs";
import Modal from "../../components/Modal";

export default function ListeUtilisateurs() {
  const [utilisateurs, setUtilisateurs] = useState([]);
  const [message, setMessage] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [userToEdit, setUserToEdit] = useState(null);
  const [newRole, setNewRole] = useState("");

  const fetchUtilisateurs = async () => {
    const res = await getUtilisateurs();
    setUtilisateurs(res);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Supprimer cet utilisateur ?")) return;
    await deleteUtilisateur(id);
    setMessage("Utilisateur supprimé.");
    fetchUtilisateurs();
  };

  const handleOpenModal = (user) => {
    setUserToEdit(user);
    setNewRole(user.role);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleUpdateRole = async () => {
    try {
      await updateUtilisateurRole(userToEdit.id, newRole);
      setMessage("Rôle modifié avec succès.");
      fetchUtilisateurs();
      handleCloseModal();
    } catch (err) {
      setMessage("Erreur lors de la modification du rôle.");
    }
  };

  useEffect(() => {
    fetchUtilisateurs();
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto min-h-screen bg-gray-950 text-white">
      <h2 className="text-3xl font-bold tracking-tight mb-6">
        Gestion des utilisateurs
      </h2>

      {message && (
        <p className="text-green-400 bg-green-900/20 border border-green-700 text-sm px-4 py-2 rounded mb-4">
          {message}
        </p>
      )}

      <div className="overflow-x-auto rounded-2xl shadow-md border border-white/10">
        <table className="w-full text-sm bg-gray-900">
          <thead className="bg-gray-800 text-white/80 text-left">
            <tr>
              <th className="px-4 py-3 font-medium">ID</th>
              <th className="px-4 py-3 font-medium">Nom</th>
              <th className="px-4 py-3 font-medium">Email</th>
              <th className="px-4 py-3 font-medium">Rôle</th>
              <th className="px-4 py-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {utilisateurs.map((u) => (
              <tr
                key={u.id}
                className="border-t border-white/10 hover:bg-white/5 transition"
              >
                <td className="px-4 py-3 text-white/90">{u.id}</td>
                <td className="px-4 py-3 text-white/90">{u.nom}</td>
                <td className="px-4 py-3 text-white/70">{u.email}</td>
                <td className="px-4 py-3 capitalize text-white/80">{u.role}</td>
                <td className="px-4 py-3 flex gap-2">
                  <button
                    onClick={() => handleOpenModal(u)}
                    className="bg-white/10 hover:bg-white/20 text-white text-xs px-3 py-1 rounded transition"
                  >
                    Modifier
                  </button>
                  <button
                    onClick={() => handleDelete(u.id)}
                    className="bg-red-600 hover:bg-red-500 text-white text-xs px-3 py-1 rounded transition"
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modale de modification de rôle */}
      {isModalOpen && (
        <Modal>
          <h3 className="text-xl font-semibold text-center mb-4 text-white/90">
            Modifier le rôle de {userToEdit.nom}
          </h3>
          <select
            className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20 mb-4"
            value={newRole}
            onChange={(e) => setNewRole(e.target.value)}
          >
            <option value="employe">Employé</option>
            <option value="technicien">Technicien</option>
            <option value="admin">Administrateur</option>
          </select>

          <div className="flex justify-between gap-2">
            <button
              onClick={handleUpdateRole}
              className="bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-md transition"
            >
              Modifier
            </button>
            <button
              onClick={handleCloseModal}
              className="bg-red-700 hover:bg-red-600 text-white px-4 py-2 rounded-md transition"
            >
              Annuler
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}
