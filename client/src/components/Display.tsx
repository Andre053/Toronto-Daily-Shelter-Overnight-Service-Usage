'use client'
import { useEffect, useState } from "react";
import { DataByMonth, ServerData, GeoData, MonthlyStatsFsa, AllStatsFsa } from "@/types/Data";
import { MapFsa, MapSettings } from "./DisplayMap";
import { Stats } from "fs";

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
async function getFsaStats(getFsaStats: any) {
  await fetch('http://localhost:8080/data/fsa/all')
        .then(res => res.json())
        .then((resJson: ServerData) => {
            const data: AllStatsFsa[] = resJson.data
            getFsaStats(data)
        })
}
export function Display() {
    const [fsaStats, setFsaStats] = useState<AllStatsFsa[] | null>(null);
    const [geoData, setGeoData] = useState<GeoData | null>(null);
    const [selectedArea, setSelectedArea] = useState<string | null>(null);
    const [startDate, setStartDate] = useState<string | null>(null);
    const [endDate, setEndDate] = useState<string | null>(null);

    // set data
    useEffect(() => {
        if (geoData || fsaStats) return;

        getGeoData('/geodata/fsa', setGeoData)
        getFsaStats(setFsaStats)

        console.log({fsaStats})
    })

    return (
        <>
            {geoData && 
                <div className="text-center align-top">
                    <MapFsa
                        width={1000}
                        height={800}
                        geoData={geoData}
                        setSelectedArea={setSelectedArea}
                    />
                </div>
            }
            {fsaStats && 
                <div className="text-left">
                    <MapSettings
                        selectedArea={selectedArea}
                        mapData={fsaStats}
                    />
                </div>
            }
        </>
    )

}