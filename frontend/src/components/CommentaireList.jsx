import { useEffect, useState, useContext } from "react";
import {
  getCommentairesByTicket,
  addCommentaire,
  updateCommentaire,
  deleteCommentaire,
} from "../api/commentaires";
import { AuthContext } from "../context/AuthContext";
import dayjs from "dayjs";
import "dayjs/locale/fr";

dayjs.locale("fr");

export default function CommentaireList({ ticketId }) {
  const { user } = useContext(AuthContext);
  const [commentaires, setCommentaires] = useState([]);
  const [contenu, setContenu] = useState("");
  const [updatedContent, setUpdatedContent] = useState("");
  const [isEditing, setIsEditing] = useState(null);

  const fetchCommentaires = async () => {
    const res = await getCommentairesByTicket(ticketId);
    setCommentaires(res);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!contenu.trim()) return;
    await addCommentaire(ticketId, contenu);
    setContenu("");
    fetchCommentaires();
  };

  const handleUpdate = async (commentaireId) => {
    try {
      await updateCommentaire(ticketId, commentaireId, updatedContent);
      setCommentaires(
        commentaires.map((c) =>
          c.id === commentaireId ? { ...c, contenu: updatedContent } : c
        )
      );
      setIsEditing(null);
      setUpdatedContent("");
    } catch (error) {
      console.error("Erreur lors de la modification du commentaire", error);
    }
  };

  const handleDelete = async (commentaireId) => {
    try {
      await deleteCommentaire(ticketId, commentaireId);
      setCommentaires(commentaires.filter((c) => c.id !== commentaireId));
    } catch (error) {
      console.error("Erreur lors de la suppression du commentaire", error);
    }
  };

  useEffect(() => {
    fetchCommentaires();
  }, [ticketId]);

  return (
    <div className="mt-10 bg-gray-950 p-6 rounded-2xl border border-white/10 shadow-lg">
      <h3 className="text-xl font-bold text-white mb-4 tracking-wide">
        Commentaires
      </h3>

      {commentaires.length === 0 && (
        <p className="text-sm text-gray-500 italic">
          Aucun commentaire pour le moment.
        </p>
      )}

      <ul className="space-y-4 mb-6">
        {commentaires.map((c) => (
          <li
            key={c.id}
            className="bg-gray-900 border border-gray-800 rounded-xl p-4 text-white"
          >
            <div className="text-sm whitespace-pre-wrap">
              {isEditing === c.id ? (
                <div>
                  <textarea
                    value={updatedContent}
                    onChange={(e) => setUpdatedContent(e.target.value)}
                    className="w-full bg-gray-800 text-white border border-white/10 px-4 py-2 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-white/20"
                  />
                  <div className="flex gap-2 mt-3">
                    <button
                      onClick={() => handleUpdate(c.id)}
                      className="bg-green-600 hover:bg-green-500 text-white px-4 py-1.5 rounded-md transition"
                    >
                      Sauvegarder
                    </button>
                    <button
                      onClick={() => setIsEditing(null)}
                      className="bg-red-600 hover:bg-red-500 text-white px-4 py-1.5 rounded-md transition"
                    >
                      Annuler
                    </button>
                  </div>
                </div>
              ) : (
                c.contenu
              )}
            </div>

            <div className="text-xs text-gray-500 mt-3">
              Posté le {dayjs(c.date_commentaire).format("DD/MM/YYYY HH:mm")} —{" "}
              <span className="text-gray-400">
                utilisateur #{c.id_utilisateur}
              </span>
            </div>

            {(user?.id === c.id_utilisateur || user?.role === "admin") && (
              <div className="flex justify-end gap-2 mt-3">
                {isEditing !== c.id && (
                  <button
                    onClick={() => {
                      setIsEditing(c.id);
                      setUpdatedContent(c.contenu);
                    }}
                    className="bg-white/10 hover:bg-white/20 text-white px-4 py-1.5 rounded-md transition"
                  >
                    Modifier
                  </button>
                )}
                <button
                  onClick={() => handleDelete(c.id)}
                  className="bg-red-700 hover:bg-red-600 text-white px-4 py-1.5 rounded-md transition"
                >
                  Supprimer
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>

      <form onSubmit={handleSubmit} className="space-y-3">
        <textarea
          value={contenu}
          onChange={(e) => setContenu(e.target.value)}
          placeholder="Ajouter un commentaire..."
          className="w-full bg-gray-900 text-white border border-white/10 px-4 py-3 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-white/20"
          rows={4}
        />
        <button
          type="submit"
          className="bg-white/10 hover:bg-white/20 text-white px-5 py-2 rounded-md transition"
        >
          Envoyer
        </button>
      </form>
    </div>
  );
}
