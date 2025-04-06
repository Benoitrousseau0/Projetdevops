// src/App.jsx
import { useContext } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from "react-router-dom";
import { AuthProvider, AuthContext } from "./context/AuthContext";

// Pages
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import TicketList from "./pages/Tickets/TicketList";
import TicketDetails from "./pages/Tickets/TicketDetails";
import CreateTicket from "./pages/Tickets/CreateTicket";
import Profil from "./pages/Profil/Profil";
import ListeUtilisateurs from "./pages/Utilisateurs/ListeUtilisateurs";
import NotificationsPage from "./pages/Notifications";
import ChangePassword from "./pages/Profil/ChangePassword";
import Dashboard from "./pages/Dashboard/Dashboard";

// Composants
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import PrivateRoute from "./components/PrivateRoute";

function AppRoutes() {
  const { user, loading } = useContext(AuthContext);
  const location = useLocation();

  const isAuthPage = location.pathname === "/login";

  if (loading) return <div className="p-10 text-center text-white">Chargement...</div>;

  if (!user && !isAuthPage) return <Navigate to="/login" />;

  return (
    <>
      {!isAuthPage && <Sidebar />}
      {!isAuthPage && <Navbar />}
      <div className={`${!isAuthPage ? "ml-64 mt-20" : ""}`}>
        <main className="p-6">
          <Routes>
            <Route path="/login" element={<LoginPage />} />

            {/* Pages protégées */}
            <Route path="/tickets" element={<PrivateRoute element={<TicketList />} />} />
            <Route path="/tickets/nouveau" element={<PrivateRoute element={<CreateTicket />} />} />
            <Route path="/tickets/:id" element={<PrivateRoute element={<TicketDetails />} />} />
            <Route path="/profil" element={<PrivateRoute element={<Profil />} />} />
            <Route path="/notifications" element={<PrivateRoute element={<NotificationsPage />} />} />
            <Route path="/profil/mot-de-passe" element={<PrivateRoute element={<ChangePassword />} />} />

            {user?.role === "admin" && (
              <>
                <Route path="/utilisateurs" element={<PrivateRoute element={<ListeUtilisateurs />} />} />
                <Route path="/dashboard" element={<PrivateRoute element={<Dashboard />} />} />
                <Route path="/register" element={<PrivateRoute element={<RegisterPage />} />} />
              </>
            )}

            <Route path="*" element={<Navigate to="/tickets" />} />
          </Routes>
        </main>
      </div>
    </>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AuthProvider>
  );
}
