'use client'

import { useEffect, useState, createContext } from "react";
import '../app/globals.css';
import { GeoData } from "@/types/Data";
import { GeoMap } from "./Map"; 
import dayjs from "dayjs";
import { MapOptions } from "./ExploreOptions";
import { MapData } from "./MapData";
import { DatePickers } from "./DatePicker";
import { ServiceUserDataAll } from "@/types/Data";
import { VisualizationTabs } from "./Tabs";
import { ThemeContext } from "@emotion/react";
import { ExploreDisplay } from "./ExploreDisplay";

/*
    Map.tsx
    - Contains the parent map component, some high-level state
*/

type Props = {
    initialGeoData: GeoData;
}

export const TabContext = createContext<any>(null);

export function Map({ initialGeoData }: Props) {

    const [isFsa, setIsFsa] = useState(initialGeoData.name === 'toronto_fsa_codes_generated')
    const [geoData, setGeoData] = useState(initialGeoData)
    const [selectedTab, setSelectedTab] = useState('tab-overview')

    const [startDate, setStartDate] = useState(dayjs('2025-01-01'));
    const [endDate, setEndDate] = useState(dayjs());
    const [mapGenerated, setMapGenerated] = useState(false)
    const [selectedArea, setSelectedArea] = useState('');
    const [filterData, setFilterData] = useState<ServiceUserDataAll | null>(null); // data for colouring the map
    

    const [width, setWidth] = useState(0)
    const [height, setHeight] = useState(0)

    // set width and height for child component
    useEffect(() => {
        const windowHeight = window.innerHeight
        setHeight(windowHeight);
        setWidth(windowHeight)
        console.log('[Map] Passing down width', width, ' and height', height)
    }, [])

    useEffect(() => {
        const url = isFsa ? "http://localhost:8080/geodata/fsa" : "http://localhost:8080/geodata/neighbourhood"
        const fc = async () => {
            const data = await fetch(url)
                .then((res) => res.json())
                .then((servData) => servData.data)
            setGeoData({
                name: data.name,
                featureCollection: data
            })
        } 
        fc()     
    }, [isFsa])

    const styles = `w-${width} h-${height} border-4 bg-gray-200 p-5`

    // TODO: Add back in date pickers to select timeline
    //<DatePickers startDate={startDate} endDate={endDate} setStartDate={setStartDate} setEndDate={setEndDate}/><br/>

    return (
        <TabContext value={{selectedTab, setSelectedTab}}>
            <h1 className="text-[36px] mb-4 mt-4">Exploration tool</h1>
            <div id='geomap-container' className='grid content-center grid-cols-2 gap-5 ml-10 mr-10'>
                <div className={styles}>
                    <VisualizationTabs
                        width={width} 
                        height={height} 
                        geoData={geoData} 
                        filterData={filterData} 
                        setFilterData={setFilterData} isFsa={isFsa} 
                        setSelectedArea={setSelectedArea}
                        setMapGenerated={setMapGenerated}
                    />
                </div>
                <div className='flex flex-wrap content-start gap-4 border-4 bg-gray-200 p-5'>
                    <ExploreDisplay
                        filterData={filterData}
                        isFsa={isFsa}
                        setIsFsa={setIsFsa}
                        mapGenerated={mapGenerated}
                        selectedArea={selectedArea}
                    />
                </div>
            </div>
        </TabContext>
    )
}