'use client'

import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { DataByFeaturePayload, DataByFeature, DataPoint, ServerData} from "@/types/Data";
import { useState } from "react";
import { start } from "repl";
/* 
    Chart.tsx
    - Not currently implemented
    - Use to show charts such as:
        - Histograms of data like service users, separated by features such as FSA, neighbourhood, shelter, organization, etc. 
        - Line graphs of data like service users over time, fitlered by features such as FSA, program type, 
        - Pie charts of data like 
*/
const createChartData = (dataCounts: number[], dates: Date[]): DataPoint[] => {
    if (dataCounts.length !== dates.length) {
        console.log('Data mismatch', {dataCounts}, {dates});
        return [];
    }
    const dataPoints: DataPoint[] = [];
    for (let i = 0; i <dataCounts.length; i++) {
        const dp: DataPoint = {
            value: dataCounts[i],
            date: dates[i]
        }
        dataPoints.push(dp);
    }
    return dataPoints
}
const dateParse = (dateStr: string) => {
    const dateParts = dateStr.split('-')
    const y = +dateParts[0]
    const m = +dateParts[1] - 1
    const d = +dateParts[2]

    const createdDate = new Date(y, m, d);

    console.log("Created", createdDate, 'from', dateStr);
    return createdDate
}

const dateAddDays = (date: Date, days: number) => {
    date.setDate(date.getDate() + days);
    return date;
}
const getDateList = (start: Date, end: Date) => {
    let dateArray: Date[] = [];

    let currentDate = start;
    console.log('Creating date array with start and end', {start}, {end})
    while (currentDate <= end) {
        dateArray.push(new Date(currentDate))
        currentDate = dateAddDays(currentDate, 1)
    }
    return dateArray;
}

type Props = {
    width: number;
    height: number;
}

export function LineChart({width, height }: Props) {
    const svgRef = useRef<SVGSVGElement | null>(null);

    const [data, setData] = useState<DataByFeature | null>(null)
    const [statName, setStatName] = useState('')
    const [startDate, setStartDate] = useState<Date | null>(null)
    const [endDate, setEndDate] = useState<Date | null>(null)
    
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
                        const data: DataByFeaturePayload = payload.data
                        setStatName(data.statName)
                        setStartDate(dateParse(data.startDate))
                        setEndDate(dateParse(data.endDate))
                        setData(data.dataByFeature)
                    } else console.log('Error setting date', {payload})
                })
        }
        getData()
    }, [])
    useEffect(() => {
        if (!data || !startDate || !endDate || !width || !height) return; // wait until all are set

        const margin = { top: 50, right: 10, bottom:20, left: 50}
        const w = width-margin.left-margin.right 
        const h = height-margin.top-margin.bottom
        
        // data to use
        // TODO: Create a radio selection
        const filteredData = data['costi_reception_centre_40'] // for testing
        const dates = getDateList(startDate, endDate);

        const chartData = createChartData(filteredData, dates); // combine

        if (chartData.length == 0) return;
        
        console.log("Chart data created", {chartData})
        const tooltip = d3.select('#chart-container') 
            .append('div')
            .attr('id', 'tooltip-chart')
            .style('position', 'absolute')
            .style('visibility', 'hidden')
            .style('font-weight', 'bold')
            .style('text-color', 'white')
            .style('opacity', 0.75)

        const svg = d3.select(svgRef.current);
        
        // size of SVG container
        // when smaller, match becomes larger
        svg
            .attr('width', width)
            .attr('height', height)

        // want multiple g elements for each part
        const gBody = d3.select(svgRef.current)
            .append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`)

        // set axis scales
        const dateRange = d3.extent(dates) as Date[];
        const maxValue = d3.max(filteredData) as number;
        const minValue = d3.min(filteredData) as number;

        const xScale = d3.scaleTime() // using dates
            .range([0, w])
        const yScale = d3.scaleLinear()
            .range([h, 0]);
            
        xScale.domain(dateRange) // d3.extent can also find this
        yScale.domain([minValue-25, maxValue+25]) 
        
        gBody.append('g')
            .attr('transform', `translate(0,${h})`) // transform group to the bottom
            .call(d3.axisBottom(xScale)
                .ticks(d3.timeMonth.every(1)))
            //.ticks(10)) // only want 10 ticks
        gBody.append('g')
            .call(d3.axisLeft(yScale)
                .ticks(10))
        
        const lineVal: any = d3.line()
            .x((d: any) => xScale(d.date))
            .y((d: any) => yScale(d.value))

        gBody.append('path') // single path to show the line
            .datum(chartData) // binds data to a single element, no need to enter
            .attr('fill', 'none') // have original map be white? gray?
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 5)
            .attr('d', lineVal)

        // circle element needs to be part of gBody
        const circle = gBody.append('circle')
            .attr('r', 0) // radius of zero
            .attr('fill', 'green')
            .style('stroke', 'white')
            .attr('opacity', 0.7)
            .style('pointer-events', 'none')

        const listeningRect = gBody.append('rect') // vertical rect to show the value when hovering over
            .attr('width', w)
            .attr('height', h)
            .attr('opacity', 0)
            .attr('z-index', 1);

        listeningRect.on('mousemove', (e: any) => {
            const [xCoordinate] = d3.pointer(e, this);
            const bisectDate = d3.bisector((d: DataPoint) => d.date).left
            const x0 = xScale.invert(xCoordinate) // data value where the mouse is
            const i = bisectDate(chartData, x0, 1); // bisect to get the date index
            const d0 = chartData[i-1] // find the two closest data points and select them, then calculate which is closer
            const d1 = chartData[i]
            const d = x0 - d0.date > d1.date - x0 ? d1 : d0; // find the closest data point
            const xPos = xScale(d.date); // these are diving the wrong coordinates
            const yPos = yScale(d.value);

            // while on the rect, show the circle at the position on the data line
            // TODO: Data seems to be correct, but position is wrong
            circle 
                .attr('cx', xPos)
                .attr('cy', yPos)
                .transition()
                .duration(50)
                .attr('r', 5);

            // TODO: xPos and yPos work for the circle, not the tooltip... need its parent to be relative
            tooltip
                .style('display', 'block')
                .style('left', `${xPos}px`) // this got the client position before
                .style('top', `${yPos}px`)
                .style('visibility', 'visible')
                .text(`Date: ${d.date.toLocaleDateString()} Population: ${d.value}`)
                
        })
    }, [data, width, height])
    return (
        <>
            <h1 className="text-[24px] my-5">Total service users by shelter over time</h1>
            <div id='chart-container' className="relative">
                <svg ref={svgRef}/>
            </div>
        </>
    )
}