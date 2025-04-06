import { useState } from "react";
import { registerUtilisateur } from "../api/utilisateurs";
import { useNavigate } from "react-router-dom";

export default function CreateUserPage() {
  const navigate = useNavigate();
  const [nom, setNom] = useState("");
  const [email, setEmail] = useState("");
  const [motDePasse, setMotDePasse] = useState("");
  const [erreur, setErreur] = useState(null);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUtilisateur({ nom, email, mot_de_passe: motDePasse });
      setMessage("Utilisateur créé avec succès !");
      setTimeout(() => navigate("/utilisateurs"), 2000);
    } catch (err) {
      setErreur("Erreur lors de la création de l'utilisateur.");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto min-h-screen bg-gray-950 text-white">
      <h2 className="text-3xl font-bold tracking-tight mb-6">
        Créer un utilisateur
      </h2>

      {erreur && (
        <div className="text-red-400 text-sm text-center bg-red-900/20 border border-red-700 p-2 rounded mb-4">
          {erreur}
        </div>
      )}
      {message && (
        <div className="text-green-400 text-sm text-center bg-green-900/20 border border-green-700 p-2 rounded mb-4">
          {message}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        className="bg-gray-900 p-6 rounded-2xl shadow-md space-y-5 border border-white/10"
      >
        <div>
          <label className="block text-sm text-white/70 mb-1">Nom</label>
          <input
            type="text"
            value={nom}
            onChange={(e) => setNom(e.target.value)}
            className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
            required
          />
        </div>

        <div>
          <label className="block text-sm text-white/70 mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
            required
          />
        </div>

        <div>
          <label className="block text-sm text-white/70 mb-1">Mot de passe</label>
          <input
            type="password"
            value={motDePasse}
            onChange={(e) => setMotDePasse(e.target.value)}
            className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
            required
          />
        </div>

        <button
          type="submit"
          className="w-full bg-white/10 hover:bg-white/20 text-white py-2 rounded-md transition"
        >
          Créer l'utilisateur
        </button>
      </form>
    </div>
  );
}
