import { Box, Tabs, Tab } from "@mui/material";
import { GeoData } from "@/types/Data";
import { GeoMap } from "./Map";
import { useContext, useState } from "react";
import { TabContext } from "./Explore";
import { LineChart } from "./LineChart";

function TabPanal({value, idx, children}: {value: string, idx: string, children: React.ReactNode}) {
    const active = value === idx

    return (
        <div className={active ? '' : 'hidden'}>
            {children}
        </div>
    )
}

type Props = {
    width: number;
    height: number;
    geoData: GeoData;
    setSelectedArea: any;
    filterData: any;
    setFilterData: any;
}

export function VisualizationTabs({width, height, geoData, filterData, setFilterData, setSelectedArea}: Props) {
    const {selectedTab, setSelectedTab} = useContext(TabContext); // TODO: May be a better way

    const handleChange = (e: any, v: any) => {
        setSelectedTab(v)
    }

    return (
        <>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs value={selectedTab} onChange={handleChange} aria-label="visualization tabs">
                    <Tab label="Overview" value='tab-overview' />
                    <Tab label="Map" value='tab-map'/>
                    <Tab label="Line chart" value='tab-line' />
                </Tabs>
            </Box>
            <TabPanal value={selectedTab} idx='tab-overview'>
                <div className='grid items-center p-5'>
                    <p>
                        Use the tabs to switch between visualizations
                        
                    </p>
                    <ul className='list-disc p-2'>
                        <li>
                            <b>Map</b> will show the map of Toronto, separated by Forward Sortation Address (FSA)
                        </li>
                        <li>
                            <b>Line</b> will show line charts based on the data selected in options
                        </li>
                    </ul>
                    
                </div>
                
            </TabPanal>
            <TabPanal value={selectedTab} idx='tab-map'>
                <GeoMap 
                    width={width} 
                    height={height} 
                    geoData={geoData} 
                    filterData={filterData} 
                    setFilterData={setFilterData} 
                    setSelectedArea={setSelectedArea} 
                />
            </TabPanal>
            <TabPanal value={selectedTab} idx='tab-line'>
                <LineChart allData={filterData} width={width} height={height}/>
            </TabPanal>
        </>
    )
}

/**
 * 
 * 
 * 
 * 








 */