import { useEffect, useState } from "react";
import '../app/globals.css';
import { ServerData, Stats, StatByFsa, AllStatsFsa, StatsKey } from "@/types/Data";
import * as d3 from "d3";
import { setUrlDateParams } from "./DisplayPage";

type HeatmapData = {
    statName: StatsKey;
    statMax: number;
    statMin: number;
    stats: StatByFsa;
}

async function getOverallStats(setOverallStats: any, urlParams: string) {
  await fetch(`http://localhost:8080/data/all/all${urlParams}`)
        .then(res => res.json())
        .then((resJson: ServerData) => {
            const data: AllStatsFsa = resJson.data
            setOverallStats(data.STATS)
        })
}
const getColour = (colourStart: string, colourEnd: string, value: number, max: number, min: number) => {
    const colourScale = d3.scaleLinear([min, max], [colourStart, colourEnd])
    return colourScale(value)
}
const setPathColour = (data: HeatmapData) => {
    const g = d3.select('#map-group'); // should only be a single g tag

    g.selectAll('path') // go through all paths and change the colour
        .classed('stroke-black', true)
        .attr('fill', (d: any) => {
            const fsa: string = d.properties.CFSAUID;
            const fsaData = data.stats[fsa];
            if (fsaData) return getColour('#fdbb84', '#e34a33', fsaData, data.statMax, data.statMin);
            return 'gray';
        })
    g.style('visibility', 'visible') // make visible once recoloured
}
const getHeatmapData = (stat: StatsKey, mapData: AllStatsFsa[]): HeatmapData => {
    const heatmapData: HeatmapData = {
        statName: stat,
        statMax: 0,
        statMin: 10000,
        stats: {}
    }
    const statByFsa: StatByFsa = {}
    mapData.forEach(v => {
            const curStat = v.STATS[stat]
            statByFsa[v.FSA] = curStat; // TODO: Type error, fix
            if (heatmapData.statMax < curStat) heatmapData.statMax = curStat;
            if (heatmapData.statMin > curStat) heatmapData.statMin = curStat;
        });

    heatmapData.stats = statByFsa;
    return heatmapData
}
type Props = {
    selectedArea: string | null;
    mapData: AllStatsFsa[];
    startDate: string | null;
    endDate: string | null;
    setStartDate: any;
    setEndDate: any;
}
export function MapSettings({selectedArea, mapData, startDate, endDate, setStartDate, setEndDate}: Props) {
    const [selectedAreaData, setSelectedAreaData] = useState<AllStatsFsa | null>(null);
    const [selectedHeatmapOption, setSelectedHeatmapOption] = useState<StatsKey>('MEAN_SERVICE_USERS')
    const [heatmapData, setHeatmapData] = useState<HeatmapData | null>(null); 
    const [overallStats, setOverallStats] = useState<Stats | null>(null);
    
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1)
    const maxDate = yesterday.toISOString().split('T')[0];

    const onChange = (e: any) => {
        setSelectedHeatmapOption(e.target.value)
        setHeatmapData(null)
        console.log('Set selected heatmap option to', e.target.value)
    }
    const startOnInput = (e: any) => {
        console.log(e.target.value, {e})
        setStartDate(e.target.value)
    }
    const endOnInput = (e: any) => {
        setEndDate(e.target.value)
    }
    useEffect(() => {
        console.log("[SETTINGS] start or end date changed, resetting stats")
        setHeatmapData(null) // must get heatmap data again
        getOverallStats(setOverallStats, setUrlDateParams(startDate, endDate));
    }, [startDate, endDate, mapData])

    useEffect(() => {
        if (!selectedArea) return;
        console.log('[SETTINGS] Building selected area data with', {mapData})
        
        let set = false;
        mapData.forEach(v => {
            if (v.FSA == selectedArea) { 
                setSelectedAreaData(v);
                set = true;
            };
        });
        if (!set) setSelectedAreaData(null);
    }, [selectedArea, mapData]);
    
    useEffect(() => { // should run on first time, colouring the map, then run on subsequent when changing
        // heat map data is within the mapData

        if (!heatmapData) {
            console.log('[SETTINGS] setting new heatmap with data', {mapData})
            setHeatmapData(getHeatmapData(selectedHeatmapOption, mapData))
        } else {
            setPathColour(heatmapData)
        }
    }, [selectedHeatmapOption, heatmapData, mapData]);
    return (
        <>
            <div className="mx-5 border rounded-4xl text-center bg-blue-400 text-gray-800 p-3">
                <h1 className="text-2xl py-2">Map Settings</h1>
                <h1 className="text-1xl py-2">Heatmap statistic</h1>
                <select 
                    id="selected-info"
                    name="selectedInfo" 
                    className="p-1 border-black border-2 text-center rounded-full"
                    onChange={onChange}
                >
                    <option value="MEAN_SERVICE_USERS">Service users</option>
                    <option value="MEAN_OCCUPIED_BEDS">Occupied beds</option>
                    <option value="MEAN_UNOCCUPIED_BEDS">Unoccupied beds</option>
                    <option value="MEAN_OCCUPIED_ROOMS">Occupied rooms</option>
                    <option value="MEAN_UNOCCUPIED_ROOMS">Unoccupied rooms</option>
                    <option value="UNIQUE_ORG_COUNT">Active organizations</option>
                    <option value="UNIQUE_PROGRAM_COUNT">Active programs</option>
                    <option value="UNIQUE_LOCATION_COUNT">Active shelters</option>
                </select>
                <h1 className="text-1xl py-2">Date range</h1>
                <input onInput={startOnInput} className="p-1 my-1 border rounded-full" type="date" id="start-date" defaultValue="2021-01-01" min="2021-01-01" max={maxDate}/><br/>
                <input onInput={endOnInput} className="p-1 my-1 border rounded-full" type="date" id="end-date" defaultValue={maxDate} min="2021-01-01" max={maxDate}/>
            </div>
            <div className="border rounded-4xl text-center bg-blue-400 text-gray-800 p-3">
                {overallStats && (
                    <>
                        <h1 className="text-2xl p-2">Overall statistics</h1>
                        <ul className='list-disc text-left ml-6'>
                            <li>There are {overallStats.MEAN_SERVICE_USERS} average service users across the city each day</li>
                            <li>Every day there are on average {overallStats.UNIQUE_SHELTER_COUNT} active shelters, {overallStats.UNIQUE_ORG_COUNT} active organizations,<br/> and {overallStats.UNIQUE_PROGRAM_COUNT} active programs on average</li>
                            <li>Programs providing beds have {overallStats.MEAN_OCCUPIED_BEDS} occupied, {overallStats.MAX_UNOCCUPIED_BEDS} unoccupied on average</li>
                            <li>Programs providing rooms have {overallStats.MAX_OCCUPIED_ROOMS} occupied, {overallStats.MAX_UNOCCUPIED_ROOMS} unoccupied on average</li>
                            <li>The most service users supported in one day was {overallStats.MAX_SERVICE_USERS}</li>
                        </ul>
                    </>
                    
                )}
            </div>
            <div className="mx-5 border rounded-4xl text-center bg-blue-400 text-gray-800 p-3">
                <h1 className="text-xl p-2">FSA statistics</h1>
                <div className="">
                    {selectedArea ? ((selectedAreaData) ? (Object.keys(selectedAreaData).length !== 0) ? (
                        <>
                            <ul className='list-disc text-left ml-6'>
                                {selectedAreaData.STATS.MEAN_SERVICE_USERS !== 0 && <li>{selectedAreaData.STATS.MEAN_SERVICE_USERS} average service users per day</li>}
                                {selectedAreaData.STATS.MEAN_OCCUPIED_BEDS !== 0 &&<li>{selectedAreaData.STATS.MEAN_OCCUPIED_BEDS} average occupied beds per day</li>}
                                {selectedAreaData.STATS.MEAN_UNOCCUPIED_BEDS !== 0 &&<li>{selectedAreaData.STATS.MEAN_UNOCCUPIED_BEDS} average unoccupied beds per day</li>}
                                {selectedAreaData.STATS.MEAN_OCCUPIED_ROOMS !== 0 &&<li>{selectedAreaData.STATS.MEAN_OCCUPIED_ROOMS} average occupied rooms per day</li>}
                                {selectedAreaData.STATS.MEAN_UNOCCUPIED_ROOMS !== 0 &&<li>{selectedAreaData.STATS.MEAN_UNOCCUPIED_ROOMS} average unoccupied rooms per day</li>}
                                {selectedAreaData.STATS.UNIQUE_PROGRAM_COUNT !== 0 &&<li>{selectedAreaData.STATS.UNIQUE_PROGRAM_COUNT} active programs</li>}
                                {selectedAreaData.STATS.UNIQUE_ORG_COUNT !== 0 &&<li>{selectedAreaData.STATS.UNIQUE_ORG_COUNT} active organizations</li>}
                                {selectedAreaData.STATS.UNIQUE_SHELTER_COUNT !== 0 &&<li>{selectedAreaData.STATS.UNIQUE_SHELTER_COUNT} active shelters</li>}
                            </ul>
                        </>
                    ) : (<>No data found...</>) : (<>Loading...</>)) : <>Select an FSA on the map...</>} 
                </div>
            </div>
            
        </>
    )
}