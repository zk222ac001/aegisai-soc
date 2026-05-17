import { useEffect, useState } from "react";
import axios from "axios";

export default function ThreatIntelTable() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);  
  // FETCH DATA
  const fetchThreatIntel = async () => {

    try {
      setLoading(true);
      const res = await axios.get("http://127.0.0.1:8000/alerts");
      const data = res.data.data || res.data || [];
      // SAFE ASYNC UPDATE
      queueMicrotask(() => {
        setAlerts(data);
      });

    } catch (error) {
      console.error(
        "Threat Intel Fetch Error:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  // EFFECT
  useEffect(() => {
    let mounted = true;
    const loadData = async () => {
      if (mounted) {
        await fetchThreatIntel();
      }
    };
    loadData();
    return () => {
      mounted = false;
    };

  }, []);

  return (
    <div className="bg-slate-900 rounded-2xl p-6 mt-6">
      {/* HEADER */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-white">
          Threat Intelligence Feed
        </h2>
        <button
          onClick={fetchThreatIntel}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-white"
        >
          Refresh
        </button>
      </div>

      {/* LOADING */}
      {loading && (
        <div className="text-cyan-400 mb-4">
          Loading threat intelligence...
        </div>
      )}

      {/* TABLE */}
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm text-left text-gray-300">
          <thead className="bg-slate-800 text-xs uppercase">
            <tr>
              <th className="px-4 py-3">IP Address</th>
              <th className="px-4 py-3">Severity</th>
              <th className="px-4 py-3">Reputation</th>
              <th className="px-4 py-3">Country</th>
              <th className="px-4 py-3">Abuse Score</th>
              <th className="px-4 py-3">AI Score</th>
            </tr>
          </thead>
          <tbody>
            {alerts.length > 0 ? (
              alerts.map((alert, index) => (
                <tr
                  key={index}
                  className="border-b border-slate-700 hover:bg-slate-800"
                >
                  <td className="px-4 py-3 font-mono">
                    {alert.ip || "Unknown"}
                  </td>

                  <td className="px-4 py-3">
                    {alert.severity || "N/A"}
                  </td>

                  <td className="px-4 py-3">
                    {alert.reputation || "Unknown"}
                  </td>

                  <td className="px-4 py-3">
                    {alert.country || "Unknown"}
                  </td>

                  <td className="px-4 py-3">
                    {alert.abuse_score || 0}
                  </td>

                  <td className="px-4 py-3">
                    {alert.ai_score || 0}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan="6"
                  className="text-center py-6 text-gray-500"
                >
                  No alerts available
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}