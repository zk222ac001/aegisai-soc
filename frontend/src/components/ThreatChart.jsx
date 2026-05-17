import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const data = [
  { time: "10:00", alerts: 5 },
  { time: "10:05", alerts: 12 },
  { time: "10:10", alerts: 8 },
];

export default function ThreatChart() {
  return (
    <div className="bg-slate-800 p-4 rounded-2xl">
      <h2 className="text-2xl font-bold mb-4">
        Threat Activity
      </h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="alerts"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}