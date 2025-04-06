import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createTicket } from "../../api/tickets";

export default function CreateTicket() {
  const navigate = useNavigate();
  const [titre, setTitre] = useState("");
  const [description, setDescription] = useState("");
  const [priorite, setPriorite] = useState("moyenne");
  const [erreur, setErreur] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createTicket({ titre, description, priorite });
      navigate("/tickets");
    } catch (err) {
      setErreur("Erreur lors de la création du ticket.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6 flex items-center justify-center">
      <div className="w-full max-w-xl bg-gray-900 border border-white/10 p-8 rounded-2xl shadow-lg">
        <h2 className="text-3xl font-bold tracking-tight mb-6">
          Créer un nouveau ticket
        </h2>

        {erreur && (
          <div className="text-red-400 text-sm mb-4 bg-red-900/20 px-4 py-2 rounded border border-red-700">
            {erreur}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm text-white/70 mb-1">Titre</label>
            <input
              type="text"
              value={titre}
              onChange={(e) => setTitre(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-white/70 mb-1">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
              rows={5}
              required
            />
          </div>

          <div>
            <label className="block text-sm text-white/70 mb-1">Priorité</label>
            <select
              value={priorite}
              onChange={(e) => setPriorite(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
            >
              <option value="faible">Faible</option>
              <option value="moyenne">Moyenne</option>
              <option value="elevee">Élevée</option>
              <option value="critique">Critique</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-white/10 hover:bg-white/20 text-white py-2 rounded-md transition"
          >
            Soumettre le ticket
          </button>
        </form>
      </div>
    </div>
  );
}
