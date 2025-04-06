import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function LoginPage() {
  const { login, user } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [motDePasse, setMotDePasse] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate("/tickets");
    }
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, motDePasse);
      navigate("/tickets");
    } catch (err) {
      setError("Adresse e-mail ou mot de passe invalide.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-black to-gray-900 text-white flex items-center justify-center px-4 py-10">
      <div className="max-w-md w-full space-y-6 bg-gray-900 border border-white/10 shadow-xl rounded-2xl p-8">
        {/* Logo + Titre */}
        <div className="flex flex-col items-center gap-2">
          <img
            src="/favicon.ico"
            alt="Logo"
            className="w-14 h-14 rounded-full bg-white/10 p-2 shadow-md"
          />
          <h1 className="text-3xl font-bold tracking-tight text-white text-center">
            Gestion des Tickets
          </h1>
          <p className="text-sm text-gray-400 text-center">
            Connectez-vous à votre espace pour gérer vos demandes.
          </p>
        </div>

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm text-white/70 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
              placeholder="exemple@domaine.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-white/70 mb-1">Mot de passe</label>
            <input
              type="password"
              value={motDePasse}
              onChange={(e) => setMotDePasse(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
              placeholder="••••••••"
              required
            />
          </div>

          {error && (
            <p className="text-sm text-red-400 bg-red-900/20 border border-red-700 px-4 py-2 rounded">
              {error}
            </p>
          )}

          <button
            type="submit"
            className="w-full bg-white/10 hover:bg-white/20 text-white py-2.5 rounded-lg font-medium transition"
          >
            Se connecter
          </button>
        </form>

        {/* Pied de page optionnel */}
        <div className="text-center text-xs text-gray-500 pt-2 border-t border-white/5">
          © {new Date().getFullYear()} Gestion des Tickets. Ferrando, Rousseau, Mallick.
        </div>
      </div>
    </div>
  );
}
