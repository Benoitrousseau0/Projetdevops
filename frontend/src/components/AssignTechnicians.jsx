import { useEffect, useState } from "react";
import axios from "../utils/axiosInstance";
import { getUtilisateurs, assignTechniciens } from "../api/utilisateurs";

export default function AssignTechnicians({ ticketId, techniciensAssignes }) {
  const [techniciens, setTechniciens] = useState([]);
  const [selection, setSelection] = useState([]);
  const [message, setMessage] = useState("");

  const fetchTechniciens = async () => {
    const res = await getUtilisateurs();
    const list = res.filter((u) => u.role === "technicien");
    setTechniciens(list);

    const alreadyAssigned = list.filter((u) =>
      techniciensAssignes.includes(u.id)
    );
    setSelection(alreadyAssigned.map((tech) => tech.id));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (selection.length === 0) return;

    try {
      await assignTechniciens(ticketId, selection);
      setMessage("Techniciens assignés avec succès.");
    } catch (error) {
      setMessage("Erreur lors de l'assignation des techniciens.");
      console.error(error);
    }
  };

  const toggleTechnicien = (id) => {
    if (selection.includes(id)) {
      setSelection((prev) => prev.filter((t) => t !== id));
      removeTechnicien(ticketId, id);
    } else {
      setSelection((prev) => [...prev, id]);
    }
  };

  const removeTechnicien = async (ticketId, technicienId) => {
    try {
      await axios.post(`/tickets/${ticketId}/desassigner?technicien_id=${technicienId}`);
      setMessage("Technicien désassigné avec succès.");
    } catch (error) {
      setMessage("Erreur lors de la désassignation du technicien.");
      console.error("Erreur lors de la désassignation du technicien", error);
    }
  };

  useEffect(() => {
    fetchTechniciens();
  }, []);

  return (
    <div className="mt-8 bg-gray-950 p-6 rounded-2xl border border-white/10 shadow-lg">
      <h3 className="text-xl font-semibold text-white mb-4 tracking-wide">
        Assigner des techniciens
      </h3>

      {techniciensAssignes?.length > 0 && (
        <div className="mb-4 text-sm text-gray-400">
          <span className="font-medium text-white">Déjà assignés :</span>{" "}
          {techniciens
            .filter((t) => techniciensAssignes.includes(t.id))
            .map((t) => t.nom)
            .join(", ") || "Chargement..."}
          <br />
          <span className="text-xs text-gray-500">
            (Décochez un nom pour désassigner)
          </span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {techniciens.map((tech) => (
            <label
              key={tech.id}
              className={`flex items-center gap-3 px-4 py-2 rounded-lg border transition cursor-pointer
                ${
                  selection.includes(tech.id)
                    ? "bg-white/5 border-white/20"
                    : "bg-gray-900 border-gray-800 hover:border-white/10"
                }
              `}
            >
              <input
                type="checkbox"
                checked={selection.includes(tech.id)}
                onChange={() => toggleTechnicien(tech.id)}
                className="accent-white h-4 w-4"
              />
              <span className="text-white text-sm">
                {tech.nom}{" "}
                <span className="text-gray-500 text-xs font-mono">#{tech.id}</span>
              </span>
            </label>
          ))}
        </div>

        <div className="flex flex-col gap-3">
          <button
            type="submit"
            className="w-fit bg-white/10 hover:bg-white/20 text-white px-5 py-2 rounded-md transition"
          >
            Assigner
          </button>

          {message && (
            <div className="text-sm text-white bg-white/5 border border-white/10 px-4 py-2 rounded">
              {message}
            </div>
          )}
        </div>
      </form>
    </div>
  );
}
