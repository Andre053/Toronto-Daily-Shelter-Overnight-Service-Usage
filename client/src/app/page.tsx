import { Button } from "@mui/material";
import torontoSkyline from "../../public/toronto-skyline.jpg"


// TODO: Initial home page is empty
// height={torontoSkyline.height} width={torontoSkyline.width}
export default async function Home() {
  console.log({torontoSkyline})
  return (
    <div className="grid grid-cols-1 text-center content-center relative bg-blue">
      <figure>
        <figcaption>
          <div className="relative">
            <img src={torontoSkyline.src} alt="Toronto skyline from Broadview avenue" className="w-full z-1" />
            <div className="absolute bg-blue w-full h-full top-0 left-0"/>
          </div>
          <span>"Toronto Skyline" by jareed. </span>
          <i>Licensed under CC BY 2.0. To view a copy of this license, visit https://creativecommons.org/licenses/by/2.0/?ref=openverse.</i>
        </figcaption>
      </figure>
      
      <div className="absolute inset-y-50 inset-x-50 text-yellow-400 font-bold">
        <h1 className="text-5xl p-5">Toronto Shelter Occupancy Application</h1><br/>
      </div>
      <div className="flex items-center justify-center gap-4 p-10">
        <Button variant="contained" size="large" href="/display">Explore the data with a map of Toronto</Button>
        <Button variant="contained" size="large" className="" href="/charts">View graphs of statistics and trends</Button>
        <Button variant="contained" size="large" className="" href="/story">Read my analysis of the data</Button>
      </div>
      
    </div>
  );
}
