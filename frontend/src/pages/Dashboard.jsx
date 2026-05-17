import AlertTable from "../components/AlertTable";
import StatsCards from "../components/StatsCards";
import LiveFeed from "../components/LiveFeed";

export default function Dashboard() {

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <h1 className="text-4xl font-bold mb-6">
        AI SOC Dashboard
      </h1>
      <StatsCards />
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <LiveFeed />
        <AlertTable />
      </div>
    </div>
  );
}