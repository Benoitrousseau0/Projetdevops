import { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { getTicketById, updateTicket } from "../../api/tickets";
import { AuthContext } from "../../context/AuthContext";
import CommentaireList from "../../components/CommentaireList";
import AssignTechnicians from "../../components/AssignTechnicians";
import dayjs from "dayjs";

export default function TicketDetails() {
  const { id } = useParams();
  const { user } = useContext(AuthContext);
  const [ticket, setTicket] = useState(null);
  const [form, setForm] = useState({});
  const [message, setMessage] = useState("");

  const fetchTicket = async () => {
    const res = await getTicketById(id);
    setTicket(res);
    setForm({
      titre: res.titre,
      description: res.description,
      priorite: res.priorite,
      statut: res.statut,
    });
  };

  useEffect(() => {
    fetchTicket();
  }, [id]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleUpdate = async () => {
    if (ticket.statut === "ferme") {
      setMessage("Ce ticket est fermé et ne peut pas être modifié.");
      return;
    }

    await updateTicket(id, form);
    setMessage("Ticket mis à jour.");
    fetchTicket();
  };

  if (!ticket) {
    return (
      <div className="min-h-screen bg-gray-950 text-white p-6">Chargement...</div>
    );
  }

  const getStatutColor = (statut) => {
    switch (statut) {
      case "ouvert":
        return "bg-blue-600";
      case "en_cours":
        return "bg-yellow-500 text-black";
      case "resolu":
        return "bg-green-600";
      case "ferme":
        return "bg-red-600";
      default:
        return "bg-gray-500";
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6 space-y-8">
      <h2 className="text-3xl font-bold tracking-tight">
        Ticket #{ticket.id}
      </h2>

      <div className="flex items-center gap-3">
        <span
          className={`text-sm font-semibold px-3 py-1 rounded-full ${getStatutColor(ticket.statut)}`}
        >
          {ticket.statut.charAt(0).toUpperCase() + ticket.statut.slice(1)}
        </span>
        <span className="text-sm text-white/60">
          Créé le{" "}
          <span className="text-white/80 font-medium">
            {dayjs(ticket.date_creation).format("DD/MM/YYYY HH:mm")}
          </span>
        </span>
      </div>

      <div className="bg-gray-900 border border-white/10 p-6 rounded-2xl shadow-md space-y-5">
        <div>
          <label className="block text-sm text-white/70 mb-1">Titre</label>
          <input
            name="titre"
            value={form.titre}
            onChange={handleChange}
            disabled={
              ticket.statut === "ferme" ||
              (user.role === "employe" && ticket.id_employe !== user.id)
            }
            className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
          />
        </div>

        <div>
          <label className="block text-sm text-white/70 mb-1">Description</label>
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            rows={4}
            disabled={
              ticket.statut === "ferme" ||
              (user.role === "employe" && ticket.id_employe !== user.id)
            }
            className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
          />
        </div>

        {user.role !== "employe" && ticket.statut !== "ferme" && (
          <div className="flex flex-wrap gap-6">
            <div>
              <label className="block text-sm text-white/70 mb-1">Statut</label>
              <select
                name="statut"
                value={form.statut}
                onChange={handleChange}
                className="bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
              >
                <option value="ouvert">Ouvert</option>
                <option value="en_cours">En cours</option>
                <option value="resolu">Résolu</option>
                <option value="ferme">Fermé</option>
              </select>
            </div>

            <div>
              <label className="block text-sm text-white/70 mb-1">Priorité</label>
              <select
                name="priorite"
                value={form.priorite}
                onChange={handleChange}
                className="bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
              >
                <option value="faible">Faible</option>
                <option value="moyenne">Moyenne</option>
                <option value="elevee">Élevée</option>
                <option value="critique">Critique</option>
              </select>
            </div>
          </div>
        )}

        {ticket.statut !== "ferme" && (
          <button
            onClick={handleUpdate}
            className="mt-2 bg-white/10 hover:bg-white/20 text-white px-5 py-2 rounded-md transition"
          >
            Sauvegarder les modifications
          </button>
        )}

        {message && (
          <p className="text-green-400 text-sm mt-3 bg-green-900/20 px-4 py-2 rounded border border-green-700">
            {message}
          </p>
        )}
      </div>

      {user.role === "admin" && (
        <AssignTechnicians
          ticketId={ticket.id}
          techniciensAssignes={ticket.techniciens}
        />
      )}

      <CommentaireList ticketId={ticket.id} />
    </div>
  );
}
