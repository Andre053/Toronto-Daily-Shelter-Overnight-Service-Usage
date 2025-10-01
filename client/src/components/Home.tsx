'use client'

import { useEffect, useState, useRef } from "react";

interface ServerData {
  message: string;
  data: string | null;
}

type DataPoint = {

}; 

export function Test({serverData}: {serverData: ServerData}) {
    const [data, setData] = useState("");
    const [msg, setMsg] = useState("Loading...");


    const svgRef = useRef<SVGSVGElement | null>(null)
    useEffect(() => {
        console.log("Use effect in Home")
        if (!serverData) return;
        setMsg(serverData.message)
        serverData.data ? setData(serverData.data) : setData("")
    }, [])
    
    return (
        <>
            <h1>SERVER TEST</h1>
            <p>Message: {msg}</p>
            {data.length > 0 && (
                <p>Data: {data}</p>
            )}
        </>
    )
}

