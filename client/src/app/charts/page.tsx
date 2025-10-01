import { fetchDataBeforeLoad } from "../utils";
import { ServerData } from "@/types/Data";

// not currently used, created for testing
// TODO: Implement initial chart data for presentation
async function getChartData() {
  const fsaRes: ServerData = await fetchDataBeforeLoad('http://localhost:3000/api/data')
  
  return { fsaRes }
}

export default async function Home() {
  const { fsaRes } = await getChartData()

  return (
    <div className="min-h-screen flex flex-col items-center">
    </div>
  );
}