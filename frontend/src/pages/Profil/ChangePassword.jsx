import { useState } from "react";
import { changePassword } from "../../api/utilisateurs";

export default function ChangePassword() {
  const [ancien, setAncien] = useState("");
  const [nouveau, setNouveau] = useState("");
  const [message, setMessage] = useState("");
  const [erreur, setErreur] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await changePassword({
        ancien_mot_de_passe: ancien,
        nouveau_mot_de_passe: nouveau,
      });
      setMessage("Mot de passe mis à jour.");
      setAncien("");
      setNouveau("");
      setErreur("");
    } catch {
      setErreur("Ancien mot de passe incorrect.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6 flex items-center justify-center">
      <div className="w-full max-w-lg bg-gray-900 p-8 rounded-2xl border border-white/10 shadow-md space-y-6">
        <h2 className="text-2xl font-bold tracking-tight">
          Changer mon mot de passe
        </h2>

        {message && (
          <p className="text-sm text-green-400 bg-green-900/20 border border-green-700 px-4 py-2 rounded">
            {message}
          </p>
        )}
        {erreur && (
          <p className="text-sm text-red-400 bg-red-900/20 border border-red-700 px-4 py-2 rounded">
            {erreur}
          </p>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm text-white/70 mb-1">
              Ancien mot de passe
            </label>
            <input
              type="password"
              value={ancien}
              onChange={(e) => setAncien(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-white/70 mb-1">
              Nouveau mot de passe
            </label>
            <input
              type="password"
              value={nouveau}
              onChange={(e) => setNouveau(e.target.value)}
              className="w-full bg-gray-800 text-white border border-white/10 px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-white/20"
              required
              minLength={8}
            />
            <p className="text-xs text-gray-500 mt-1">Minimum 8 caractères</p>
          </div>

          <button
            type="submit"
            className="w-full bg-white/10 hover:bg-white/20 text-white py-2 rounded-md transition"
          >
            Mettre à jour
          </button>
        </form>
      </div>
    </div>
  );
}
