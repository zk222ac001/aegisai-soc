import { useEffect, useState } from "react";

export default function LiveFeed() {
  const [alerts, setAlerts] = useState([]);

  // 🎨 Severity color mapping
  const severityColor = {
    low: "text-green-400",
    medium: "text-yellow-400",
    high: "text-orange-400",
    critical: "text-red-500",
  };

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/alerts");
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setAlerts((prev) => [data, ...prev.slice(0, 19)]);
      } catch (err) {
        console.error("Invalid WebSocket data:", err);
      }
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="bg-slate-800 p-4 rounded-2xl">
      <h2 className="text-2xl font-bold mb-4">
        Live Threat Feed
      </h2>

      <div className="space-y-3 max-h-[600px] overflow-auto">
        {alerts.map((alert, index) => (
          <div key={index} className="bg-slate-900 p-3 rounded-xl">
            <div className="flex justify-between">
              <span className="font-bold">
                {alert.attack_type}
              </span>

              <span className={severityColor[alert.severity] || "text-gray-400"}>
                {alert.severity}
              </span>
            </div>

            <div className="text-sm text-gray-400 mt-1">
              {alert.source_ip}
              {" → "}
              {alert.destination_ip}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}