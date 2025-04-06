import { useContext, useState } from "react";
import { AuthContext } from "../../context/AuthContext";
import { updateProfil } from "../../api/utilisateurs";
import { Link } from "react-router-dom";

export default function Profil() {
  const { user } = useContext(AuthContext);
  const [nom, setNom] = useState(user.nom);
  const [email, setEmail] = useState(user.email);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await updateProfil({ nom, email });
    setMessage("Profil mis à jour !");
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6 flex items-center justify-center">
      <div className="w-full max-w-lg bg-gray-900 p-8 rounded-2xl border border-white/10 shadow-md space-y-6">
        <h2 className="text-2xl font-bold tracking-tight">Mon profil</h2>

        {message && (
          <p className="text-sm text-green-400 bg-green-900/20 border border-green-700 px-4 py-2 rounded">
            {message}
          </p>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm text-white/70 mb-1">Nom</label>
            <input
              type="text"
              value={nom}
              onChange={(e) => setNom(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
            />
          </div>

          <div>
            <label className="block text-sm text-white/70 mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-white/10 hover:bg-white/20 text-white py-2 rounded-md transition"
          >
            Sauvegarder
          </button>
        </form>

        <div className="pt-4 border-t border-white/5 text-sm">
          <Link
            to="/profil/mot-de-passe"
            className="inline-flex items-center gap-2 text-white/70 hover:text-white hover:underline transition"
          >
            🔒 Changer mon mot de passe
          </Link>
        </div>
      </div>
    </div>
  );
}
