import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../context/AuthContext";
import { getTickets } from "../../api/tickets";
import TicketCard from "../../components/TicketCard";

export default function TicketList() {
  const { user } = useContext(AuthContext);
  const [tickets, setTickets] = useState([]);
  const [statut, setStatut] = useState("");
  const [priorite, setPriorite] = useState("");
  const [sort, setSort] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      const res = await getTickets({ statut, priorite, sort });
      setTickets(res);
    };
    fetchData();
  }, [statut, priorite, sort]);

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      <h2 className="text-3xl font-bold tracking-tight mb-8">Liste des Tickets</h2>

      {user.role === "admin" && (
        <div className="grid sm:grid-cols-3 gap-4 mb-8">
          <SelectFilter
            label="Statut"
            value={statut}
            onChange={setStatut}
            options={[
              { value: "", label: "Tous les statuts" },
              { value: "ouvert", label: "Ouvert" },
              { value: "en_cours", label: "En cours" },
              { value: "resolu", label: "Résolu" },
              { value: "ferme", label: "Fermé" },
            ]}
          />
          <SelectFilter
            label="Priorité"
            value={priorite}
            onChange={setPriorite}
            options={[
              { value: "", label: "Toutes priorités" },
              { value: "faible", label: "Faible" },
              { value: "moyenne", label: "Moyenne" },
              { value: "elevee", label: "Élevée" },
              { value: "critique", label: "Critique" },
            ]}
          />
          <SelectFilter
            label="Trier par"
            value={sort}
            onChange={setSort}
            options={[
              { value: "", label: "Par défaut" },
              { value: "date_asc", label: "Date ↑" },
              { value: "date_desc", label: "Date ↓" },
            ]}
          />
        </div>
      )}

      <div className="grid gap-4">
        {tickets.length > 0 ? (
          tickets.map((ticket) => (
            <TicketCard key={ticket.id} ticket={ticket} />
          ))
        ) : (
          <p className="text-gray-400 italic">Aucun ticket trouvé.</p>
        )}
      </div>
    </div>
  );
}

function SelectFilter({ label, value, onChange, options }) {
  return (
    <div className="flex flex-col gap-1">
      <label className="text-sm text-white/70">{label}</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="bg-gray-900 border border-white/10 text-white text-sm px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20 transition"
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}
