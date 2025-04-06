import { useEffect, useState } from "react";
import { getNotifications } from "../api/notifications";
import { Link } from "react-router-dom";
import { Bell } from "lucide-react";

export default function NotificationBadge() {
  const [count, setCount] = useState(0);

  const fetchNotifications = async () => {
    try {
      const res = await getNotifications();
      const nonLues = res.filter((notif) => !notif.lu);
      setCount(nonLues.length);
    } catch (err) {
      console.error("Erreur chargement notifications", err);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  return (
    <Link to="/notifications" className="relative group">
      <Bell className="w-6 h-6 text-white group-hover:text-white/80 transition-colors" />
      {count > 0 && (
        <span className="absolute -top-1.5 -right-2.5 bg-red-500 text-white text-[10px] px-1.5 py-0.5 rounded-full font-bold shadow-sm animate-pulse">
          {count}
        </span>
      )}
    </Link>
  );
}
