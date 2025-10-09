import { useEffect, useState } from "react";
import '../app/globals.css';
import { Stats, AllStatsFsa, ServerData } from "@/types/Data";
import { setUrlDateParams } from "./DisplayPage";
import { GraphData } from "@/types/Data";

// /data/timeseries/yearly/SERVICE_USER_COUNT
const getGraphData = async (setData: any, dataFrequency: string, stat: string, urlParams: string) => {
    console.log("Want data with frequency", dataFrequency, "and params", urlParams)
    await fetch(`http://localhost:8080/data/timeseries/${dataFrequency}/${stat}/${urlParams}`)
        .then((res) => res.json())
        .then((payload: ServerData) => {
            console.log({payload})
            setData(payload.data)
        })
}
type Props = {
    graphData: GraphData | null;
    setGraphData: any;
}
export function GraphSettings({graphData, setGraphData}: Props) {
    const [selectedGraphStat, setSelectedGraphStat] = useState<string>('SERVICE_USER_COUNT')
    const [selectedFreq, setSelectedFreq] = useState<string>('DAILY')
    const [startDate, setStartDate] = useState<string | null>(null);
    const [endDate, setEndDate] = useState<string | null>(null);
    
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1)
    const maxDate = yesterday.toISOString().split('T')[0];

    const onStatChange = (e: any) => {
        console.log('Set selected graph option to', e.target.value);
        setSelectedGraphStat(e.target.value);
        setGraphData(null)
    }
    const onFreqChange = (e: any) => {
        console.log('Set selected frequency option to', e.target.value);
        setSelectedFreq(e.target.value)
        setGraphData(null)
    }
    const startOnInput = (e: any) => {
        setStartDate(e.target.value)
        setGraphData(null)
    }
    const endOnInput = (e: any) => {
        setEndDate(e.target.value)
        setGraphData(null)
    }
    useEffect(() => {
        if (!graphData) getGraphData(setGraphData, selectedFreq, selectedGraphStat, setUrlDateParams(startDate, endDate));
    }, [startDate, endDate, selectedGraphStat, selectedFreq, graphData])

    return (
        <div className="grid grid-cols-3 gap-2 justify-center">
            <div className="border rounded-4xl text-center bg-blue-400 text-gray-800 p-3">
                <h1 className="text-2xl py-2">Graph statistic</h1>
                <p className="mb-2">Choose the statistic to map on the graph</p>
                <select 
                    id="selected-info"
                    name="selectedInfo" 
                    className="p-1 border-black border-2"
                    onChange={onStatChange}
                >
                    <option value="SERVICE_USER_COUNT">Service users</option>
                    <option value="OCCUPIED_BEDS">Occupied beds</option>
                    <option value="UNOCCUPIED_BEDS">Unoccupied beds</option>
                    <option value="OCCUPIED_ROOMS">Occupied rooms</option>
                    <option value="UNOCCUPIED_ROOMS">Unoccupied rooms</option>
                    <option value="CAPACITY_FUNDING_BEDS">Capacity funding beds</option>
                    <option value="CAPACITY_ACTUAL_BEDS">Capacity actual beds</option>
                    <option value="CAPACITY_FUNDING_ROOMS">Capacity funding rooms</option>
                    <option value="CAPACITY_ACTUAL_ROOMS">Capacity actual rooms</option>
                </select>
            </div>
            <div className="border rounded-4xl text-center bg-blue-400 text-gray-800 p-3">
                <h1 className="text-2xl py-2">Data frequency</h1>
                <p className="mb-2">Choose the how the data is averaged</p>
                <select 
                    id="selected-freq"
                    name="selectedFreq" 
                    className="p-1 border-black border-2"
                    onChange={onFreqChange}
                >
                    <option value="DAILY">By day</option>
                    <option value="MONTHLY">By month</option>
                    <option value="YEARLY">By year</option>
                </select>
            </div>
            <div className="border rounded-4xl text-center bg-blue-400 text-gray-800 p-3">
                <h1 className="text-2xl py-2">Date range</h1>
                <input onInput={startOnInput} className="p-1 my-1 border rounded-full" type="date" id="start-date" defaultValue="2021-01-01" min="2021-01-01" max={maxDate}/><br/>
                <input onInput={endOnInput} className="p-1 my-1 border rounded-full" type="date" id="end-date" defaultValue={maxDate} min="2021-01-01" max={maxDate}/>
            </div>
        </div>
    )
}