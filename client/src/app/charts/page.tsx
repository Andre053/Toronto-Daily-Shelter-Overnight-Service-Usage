import { ChartItem } from "@/components/ChartItem";
import { fetchDataBeforeLoad } from "../utils";
import { ServerData } from "@/types/Data";

// not currently used, created for testing
// TODO: Implement initial chart data for presentation
async function getChartData() {
  const fsaRes: ServerData = await fetchDataBeforeLoad('http://localhost:3000/api/data')
  
  return { fsaRes }
}

// TODO: Each chart should have chart options, similar to explore page layout?
export default async function Home() {

  return (
    <div className="min-h-screen flex flex-col items-center">
      <ChartItem/>
    </div>
  );
}