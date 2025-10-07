'use client'

import { useEffect, useState, createContext, Suspense } from "react";
import '../app/globals.css';
import { DataByMonth, GeoData, ServerData } from "@/types/Data";
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


/**
 * DATA BY MONTH
 * Retrieved from: /data/by_month
 * 
 */
export const getMonthData = async (setData: any) => {
    const url = `http://localhost:8080/data/by_month`

    fetch(url)
        .then((res) => res.json())
        .then((data: ServerData) => {
            console.log(`Monthly data: ${data.message}`)
            const monthlyData: DataByMonth = data.data
            console.log({monthlyData})
            setData(monthlyData)
        })
}


export function Map({ initialGeoData }: Props) {

    const [geoData, setGeoData] = useState(initialGeoData)
    const [selectedTab, setSelectedTab] = useState('tab-overview')

    const [startDate, setStartDate] = useState(dayjs('2025-01-01'));
    const [endDate, setEndDate] = useState(dayjs());
    const [selectedArea, setSelectedArea] = useState('');
    const [filterData, setFilterData] = useState<ServiceUserDataAll | null>(null); // data for colouring the map
    const [monthlyData, setMonthlyData] = useState<DataByMonth | null>(null)

    const [width, setWidth] = useState(0)
    const [height, setHeight] = useState(0)

    // set width and height for child component
    useEffect(() => {
        const windowHeight = window.innerHeight
        setHeight(windowHeight);
        setWidth(windowHeight)
        console.log('[Map] Passing down width', width, ' and height', height)

        getMonthData(setMonthlyData)
    }, [])

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
                        setFilterData={setFilterData} 
                        setSelectedArea={setSelectedArea}
                    />
                </div>
                <div className='flex flex-wrap content-start gap-4 border-4 bg-gray-200 p-5'>
                    <Suspense fallback={<div>Loading...</div>}>
                        <ExploreDisplay
                            filterData={filterData}
                            selectedArea={selectedArea}
                        />
                    </Suspense>
                    
                </div>
            </div>
        </TabContext>
    )
}