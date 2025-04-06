import { NavLink } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import {
  User,
  Ticket,
  Bell,
  PlusCircle,
  Users,
  LayoutDashboard,
} from "lucide-react";

export default function Sidebar() {
  const { user } = useContext(AuthContext);

  const linkClass = ({ isActive }) =>
    `relative flex items-center gap-3 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200
     ${
       isActive
         ? "text-white bg-white/10 shadow-inner before:absolute before:left-0 before:top-1/2 before:-translate-y-1/2 before:w-1 before:h-5 before:bg-white before:rounded-r"
         : "text-gray-300 hover:bg-white/5 hover:text-white"
     }`;

  return (
    <aside className="fixed top-0 left-0 h-screen w-64 bg-white/5 backdrop-blur-md border-r border-white/10 p-6 hidden md:flex flex-col z-40">
      <h2 className="text-xl font-bold text-white mb-8 tracking-wide uppercase">
        Navigation
      </h2>

      <nav className="flex flex-col gap-2">
        <NavLink to="/tickets" className={linkClass}>
          <Ticket size={18} /> Mes Tickets
        </NavLink>

        {user?.role === "employe" && (
          <NavLink to="/tickets/nouveau" className={linkClass}>
            <PlusCircle size={18} /> Nouveau Ticket
          </NavLink>
        )}

        {user?.role === "admin" && (
          <>
            <NavLink to="/utilisateurs" className={linkClass}>
              <Users size={18} /> Gérer les Utilisateurs
            </NavLink>
            <NavLink to="/register" className={linkClass}>
              <PlusCircle size={18} /> Créer un Utilisateur
            </NavLink>
            <NavLink to="/dashboard" className={linkClass}>
              <LayoutDashboard size={18} /> Tableau de bord
            </NavLink>
          </>
        )}

        <NavLink to="/notifications" className={linkClass}>
          <Bell size={18} /> Notifications
        </NavLink>

        <NavLink to="/profil" className={linkClass}>
          <User size={18} /> Mon Profil
        </NavLink>
      </nav>
    </aside>
  );
}
