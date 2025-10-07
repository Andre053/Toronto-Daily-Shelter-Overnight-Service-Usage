'use client'

import { useState, useEffect } from "react";
import { ChartOpts, ChartOption, DataByFeaturePayload, ServerData } from "@/types/Data";
import { ChartGeneric } from "./Chart";
import { ChartOptions } from "./ChartOptions";

type Props = {

}

export function ChartItem() {
    const [data, setData] = useState<DataByFeaturePayload | null>(null)
    const [options, setOptions] = useState<ChartOpts | null>(null)

    useEffect(() => {
        // load data on first run
        const getData: any = async () => {
            const statForServer = 'SERVICE_USER_COUNT';
            const featForServer = 'shelters';
            console.log('[CHART] Getting data from server')
            await fetch(`http://localhost:8080/data/all/${featForServer}/${statForServer}`)
                .then((res) => res.json())
                .then((payload: ServerData) => {
                    if (payload.message == 'Successful retrieval of feature data') {
                        setData(payload.data)
                    } else console.log('Error setting date', {payload})
                })
        }
        getData()
    }, [])

    // set chart options
    useEffect(() => {
        if (!data) return;

        const dataOptions: ChartOpts = {}
        const optionList: ChartOption[] = []

        Object.keys(data.dataByFeature).forEach((key) => {
            const opt: ChartOption = {
                selectedStatus: false,
                displayName: key.toUpperCase().replaceAll('_', ' '),
                dataKey: key
            }
            optionList.push(opt)
        })
        dataOptions[data.statName] = optionList;

        setOptions(dataOptions);

        console.log('Created option list', {dataOptions})
    }, [data]);

    return (
        <div className="h-max w-max grid grid-cols-2">
            <ChartGeneric payload={data} selectedOptions={options} />
            <ChartOptions selectedOptions={options} setSelectedOptions={setOptions}/>
        </div>
    )
}