import { useEffect, useState } from "react";
import axios from "axios";

export default function StatsCards() {
  const [stats, setStats] = useState({});

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/stats");
        console.log("API RESPONSE:", res.data);
        // 👇 FIX: support multiple API shapes
        const data = res.data.data || res.data;
        setStats(data);
      } catch (error) {
        console.error("Failed to fetch stats:", error);
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="bg-slate-800 p-5 rounded-2xl">
        <h2 className="text-gray-400">Total Alerts</h2>
        <p className="text-3xl font-bold">
          {stats.total_alerts ?? 0}
        </p>
      </div>

      <div className="bg-slate-800 p-5 rounded-2xl">
        <h2 className="text-gray-400">Critical Alerts</h2>
        <p className="text-3xl font-bold text-red-400">
          {stats.critical_alerts ?? 0}
        </p>
      </div>

      <div className="bg-slate-800 p-5 rounded-2xl">
        <h2 className="text-gray-400">AI Anomalies</h2>
        <p className="text-3xl font-bold text-yellow-400">
          {stats.ai_anomalies ?? 0}
        </p>
      </div>
    </div>
  );
}