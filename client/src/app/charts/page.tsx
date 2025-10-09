import { GraphPage } from "@/components/GraphPage";

// not currently used, created for testing
// TODO: Implement initial chart data for presentation

// TODO: Each chart should have chart options, similar to explore page layout?
export default async function Home() {

  return (
    <div className="grid grid-cols-2 items-start gap-10 m-5 h-screen">
      <GraphPage/>
    </div>
  );
}