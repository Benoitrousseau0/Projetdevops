import { useEffect, useState } from "react";
import { getDashboardStats } from "../../api/admin";

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getDashboardStats();
      setDashboardData(data);
    };
    fetchData();
  }, []);

  if (!dashboardData)
    return (
      <div className="p-10 text-center text-white text-sm opacity-70">Chargement...</div>
    );

  return (
    <div className="p-8 bg-gray-950 min-h-screen text-white">
      <h1 className="text-3xl font-bold mb-8 tracking-tight">
        Tableau de bord — Admin
      </h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Tickets ouverts */}
        <Card title="Tickets ouverts" value={dashboardData.tickets_opened} />

        {/* Tickets résolus */}
        <Card title="Tickets résolus" value={dashboardData.tickets_resolved} />

        {/* Tickets critiques */}
        <Card title="Tickets critiques" value={dashboardData.critical_tickets} highlight />

        {/* Temps moyen de résolution par technicien */}
        <div className="bg-gray-900 border border-white/10 rounded-2xl p-6 shadow-md col-span-1 sm:col-span-2 space-y-4">
          <h2 className="text-lg font-semibold text-white/90">
            Temps moyen de résolution par technicien
          </h2>

          {dashboardData.avg_resolution_time_by_technician.length > 0 ? (
            <div className="divide-y divide-white/5">
              {dashboardData.avg_resolution_time_by_technician.map(
                (technician, index) => {
                  const avgTime = technician.avg_resolution_time;
                  const formatted = isNaN(avgTime)
                    ? "N/A"
                    : avgTime.toFixed(2);

                  return (
                    <div
                      key={index}
                      className="flex justify-between py-2 text-sm text-gray-300"
                    >
                      <span className="font-medium">
                        Technicien #{technician.technicien_id}
                      </span>
                      <span>{formatted} heures</span>
                    </div>
                  );
                }
              )}
            </div>
          ) : (
            <p className="text-sm text-gray-400 italic">
              Aucun technicien trouvé
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

function Card({ title, value, highlight = false }) {
  return (
    <div
      className={`bg-gray-900 border rounded-2xl p-6 shadow-md space-y-3 ${
        highlight ? "border-red-600" : "border-white/10"
      }`}
    >
      <h2 className="text-lg font-semibold text-white/90">{title}</h2>
      <p
        className={`text-4xl font-bold tracking-tight ${
          highlight ? "text-red-400" : "text-white"
        }`}
      >
        {value}
      </p>
    </div>
  );
}
