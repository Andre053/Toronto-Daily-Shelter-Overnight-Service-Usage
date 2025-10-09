'use client'
import { useEffect, useState } from "react";
import { DataByMonth, ServerData, GeoData, MonthlyStatsFsa, AllStatsFsa } from "@/types/Data";
import { MapFsa } from "./DisplayMap";
import { MapSettings } from "./DisplayOptions";

export const setUrlDateParams = (startDate: string | null, endDate: string | null): string => {
    let urlParams = '';
    if (startDate && endDate) {
            urlParams = `?start=${startDate}&end=${endDate}`
        } else if (startDate) {
            urlParams = `?start=${startDate}`
        } else if (endDate) {
            urlParams = `?end=${endDate}`
        }
    return urlParams;
}

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
async function getFsaStats(getFsaStats: any, urlParams: string) {
  await fetch(`http://localhost:8080/data/fsa/all${urlParams}`)
        .then(res => res.json())
        .then((resJson: ServerData) => {
            const data: AllStatsFsa[] = resJson.data
            console.log("[DISPLAY] new fsa data", urlParams, {data})
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
        //if (geoData || fsaStats) return;
        if (!geoData && !fsaStats) {
            console.log(`Getting geo data with start date ${startDate} and end date ${endDate}`)
        
            getGeoData(`/geodata/fsa`, setGeoData)

            const urlParams = setUrlDateParams(startDate, endDate)
            getFsaStats(setFsaStats, urlParams)

            console.log({fsaStats})
        }
    }, [geoData, fsaStats])

    useEffect(() => {
        if (startDate || endDate) {
            console.log('Start date or end date changed, getting new fsa stats')

            const urlParams = setUrlDateParams(startDate, endDate)
            getFsaStats(setFsaStats, urlParams)
        }
    }, [startDate, endDate])

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
                        startDate={startDate}
                        endDate={endDate}
                        setStartDate={setStartDate}
                        setEndDate={setEndDate}
                    />
                </div>
            }
        </>
    )

}