'use client'

import { useState, useEffect } from "react";
import { LineChart } from "./Graph";
import { GraphSettings } from "./GraphOptions";
import { GraphData } from "@/types/Data";


export function GraphPage() {
    const [data, setData] = useState<GraphData | null>(null)
    const [options, setOptions] = useState<any| null>(null)

    useEffect(() => {
        // get data
    }, [])
    // set chart options
    useEffect(() => {
        // manage chart options
    }, [data]);

    return (
        <> 
            <h1 className="text-4xl my-3 text-center">Occupancy Statistics Over Time</h1>
            <GraphSettings graphData={data} setGraphData={setData}/>
            <LineChart data={data}/>
        </>
    )
        
    
}