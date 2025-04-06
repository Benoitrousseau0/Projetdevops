import { Link } from "react-router-dom";
import dayjs from "dayjs";
import "dayjs/locale/fr";

dayjs.locale("fr");

export default function TicketCard({ ticket }) {
  const statutColors = {
    ouvert: "bg-gray-700 text-gray-100",
    en_cours: "bg-yellow-500/20 text-yellow-300",
    resolu: "bg-green-500/20 text-green-300",
    ferme: "bg-red-500/20 text-red-300",
  };

  const prioriteColors = {
    critique: "bg-red-500/10 text-red-400",
    elevee: "bg-orange-500/10 text-orange-400",
    moyenne: "bg-yellow-500/10 text-yellow-400",
    basse: "bg-green-500/10 text-green-400",
  };

  return (
    <Link
      to={`/tickets/${ticket.id}`}
      title={`Voir le ticket : ${ticket.titre}`}
      className="block bg-gray-900 border border-gray-800 rounded-2xl p-5 hover:shadow-lg hover:border-white/20 transition duration-200"
    >
      <div className="flex justify-between items-start">
        <div className="pr-4">
          <h3 className="text-lg font-semibold text-white">{ticket.titre}</h3>
          <p className="text-sm text-gray-400 line-clamp-2">
            {ticket.description}
          </p>
        </div>

        <span
          className={`text-xs px-2 py-1 rounded-md font-medium shrink-0 ${statutColors[ticket.statut] || "bg-gray-700 text-gray-300"}`}
        >
          {ticket.statut}
        </span>
      </div>

      <div className="mt-4 text-sm flex justify-between items-center">
        <span
          className={`text-xs font-semibold px-2 py-1 rounded-md ${prioriteColors[ticket.priorite] || "bg-gray-700 text-gray-300"}`}
        >
          Priorité : {ticket.priorite}
        </span>

        <span className="text-gray-500 text-xs">
          Créé le : {dayjs(ticket.date_creation).format("DD/MM/YYYY HH:mm")}
        </span>
      </div>
    </Link>
  );
}
