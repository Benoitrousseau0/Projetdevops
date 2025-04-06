import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import NotificationBadge from "./NotificationBadge";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);

  return (
    <header className="fixed top-0 left-64 right-0 z-40 bg-gray-950/90 backdrop-blur-md border-b border-white/10 px-6 py-4 flex justify-between items-center shadow-md">

      <div className="flex items-center gap-3">
        <img
          src="/favicon.ico"
          alt="Logo"
          className="w-12 h-12 rounded-full bg-white/10 p-1 shadow-sm"
        />
        <h1 className="text-2xl font-black text-white tracking-wide uppercase">
          Gestion des Tickets
        </h1>
      </div>

      <div className="flex items-center gap-6">
        <NotificationBadge />

        <div className="text-sm text-gray-300">
          Connecté en tant que{" "}
          <span className="font-semibold text-white">{user?.nom}</span>
        </div>

        <button
          onClick={logout}
          className="bg-red-600 hover:bg-red-500 text-white text-sm px-4 py-1.5 rounded-md transition hover:shadow-md"
        >
          Déconnexion
        </button>
      </div>
    </header>
  );
}
