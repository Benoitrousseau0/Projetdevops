import { useEffect, useState } from "react";
import {
  getNotifications,
  markAsRead,
  markAllAsRead,
} from "../api/notifications";
import { Link } from "react-router-dom";
import dayjs from "dayjs";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);

  const fetchNotifications = async () => {
    const res = await getNotifications();
    setNotifications(
      res.sort((a, b) => new Date(b.date_envoi) - new Date(a.date_envoi))
    );
  };

  const handleMarkRead = async (id) => {
    await markAsRead(id);
    fetchNotifications();
  };

  const handleMarkAll = async () => {
    await markAllAsRead();
    fetchNotifications();
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <div className="max-w-3xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold tracking-tight">Notifications</h2>
          <button
            onClick={handleMarkAll}
            className="text-sm bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-md transition"
          >
            Tout marquer comme lu
          </button>
        </div>

        <div className="space-y-4">
          {notifications.length === 0 ? (
            <p className="text-gray-400 italic">Aucune notification.</p>
          ) : (
            notifications.map((notif) => (
              <div
                key={notif.id}
                className={`p-5 rounded-xl transition-all border ${
                  notif.lu
                    ? "bg-gray-900 border-white/5"
                    : "bg-white/5 border-white/10 shadow-sm"
                }`}
              >
                <div className="flex justify-between items-start gap-4">
                  <div className="flex-1">
                    <p className="text-sm text-white/90 mb-1">
                      {notif.message}
                    </p>
                    {notif.id_ticket && (
                      <Link
                        to={`/tickets/${notif.id_ticket}`}
                        className="text-sm text-white/60 hover:text-white/80 underline"
                      >
                        Voir le ticket concerné
                      </Link>
                    )}
                    <p className="text-xs text-gray-500 mt-1">
                      {dayjs(notif.date_envoi).format("DD/MM/YYYY HH:mm")}
                    </p>
                  </div>
                  {!notif.lu && (
                    <button
                      onClick={() => handleMarkRead(notif.id)}
                      className="text-xs bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-md transition"
                    >
                      Marquer comme lu
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
