'use client'
import { useEffect, useState } from "react";
import { DataByMonth, ServerData, GeoData } from "@/types/Data";
import { MapFsa, MapSettings } from "./DisplayMap";

async function getGeoData(endpoint: string, setGeoData: any) {
    await fetch(`http://localhost:8080${endpoint}`)
        .then(res => res.json())
        .then((resJson: ServerData) => {
            const resGeoData: GeoData = {
                name: resJson.data.name,
                featureCollection: resJson.data
            }
            setGeoData(resGeoData)
            console.log({resGeoData})
        })
}
async function getMonthlyData(setMonthlyData: any) {
  await fetch('http://localhost:8080/data/by_month')
        .then(res => res.json())
        .then((resJson: ServerData) => {
            const resMonthlyData: DataByMonth[] = resJson.data
            setMonthlyData(resMonthlyData)
            console.log({resMonthlyData})
        })
}
export function Display() {
    const [dataByMonth, setDataByMonth] = useState<DataByMonth[] | null>(null);
    const [geoData, setGeoData] = useState<GeoData | null>(null);
    const [selectedArea, setSelectedArea] = useState<string | null>(null);

    // set data
    useEffect(() => {
        if (geoData || dataByMonth) return;

        getGeoData('/geodata/fsa', setGeoData)
        getMonthlyData(setDataByMonth)

        console.log({geoData}, {dataByMonth})
    })

    return (
        <>
            {geoData && 
                <div className="text-center">
                    <MapFsa
                        width={800}
                        height={600}
                        geoData={geoData}
                        setSelectedArea={setSelectedArea}
                    />
                </div>
            }
            {dataByMonth && 
                <div className="text-center">
                    <MapSettings
                        selectedArea={selectedArea}
                        mapData={dataByMonth}
                    />
                </div>
            }
        </>
    )

}