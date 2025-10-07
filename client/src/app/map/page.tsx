import { Map } from "@/components/Explore";
import { fetchDataBeforeLoad } from "../utils";
import { FsaData, ServerData } from "@/types/Data";
import { GeoData } from "@/types/Data";

async function getMapData() {
  const geoRes: ServerData = await fetchDataBeforeLoad('http://localhost:3000/api/geodata')
  
  if (geoRes.message != "GeoJson data retrieved") {
    // TODO: Error handling, return some null object
    console.log("Failed to retrieve geojson") 
  }
  const initialGeoData: GeoData = {
    name: geoRes.data.name,
    featureCollection: geoRes.data
  }
  return { initialGeoData }
}

export default async function Home() {
  const { initialGeoData } = await getMapData()
  
  return (
    <div className="min-h-screen flex flex-col items-center">
      <Map initialGeoData={initialGeoData}/>
    </div>
  );
}