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
            <LineChart data={data}/>
            <GraphSettings graphData={data} setGraphData={setData}/>
        </>
    )
        
    
}