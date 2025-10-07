'use client'
import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { DataByFeaturePayload, DataByFeature, DataPoint, ChartOption, ChartOpts} from "@/types/Data";
import { useState } from "react";

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
const filterData = (data: DataByFeature, options: ChartOpts) => {
    // depending on the options chosen, filter the data
    const dataFiltered: DataByFeature = {}
    const optionKeys = Object.keys(options);
    const dataKeys = Object.keys(data);

    console.log('Filtering data', {data}, {options});

    // data is in the form key: data
    for (const key in optionKeys) {
        options[key].forEach((v) => {
            if (v.selectedStatus) {
                for (const dataKey in data) {
                    if (dataKey == v.dataKey) {
                        dataFiltered[dataKey] = data[dataKey];
                    }
                }
            }
        })
    }
    console.log('Filtered to', {dataFiltered});

    return dataFiltered;
}

type Props = {
    payload: DataByFeaturePayload | null;
    selectedOptions: ChartOpts | null;
}

// get data from parent
export function ChartGeneric({payload, selectedOptions}: Props) {

    // percentages
    const wSVG = 50;
    const hSVG = 30;

    const svgRef = useRef<SVGSVGElement | null>(null);
    const [statName, setStatName] = useState<string | null>(null)
    const [startDate, setStartDate] = useState<Date | null>(null)
    const [endDate, setEndDate] = useState<Date | null>(null)
    const [data, setData] = useState<DataByFeature | null>(null)

    const margin = { top: 1, right: 1, bottom: 1, left: 1}
    const wG = wSVG-margin.left-margin.right 
    const hG = hSVG-margin.top-margin.bottom

    const g = d3.select(svgRef.current)
            .attr('width', wG +'%')
            .attr('height', hG + '%')
            .append('g')
                .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const tooltip = d3.select('#chart-container')
        .append('div')
        .attr('id', 'tooltip-chart')
        .style('position', 'absolute')
        .style('visibility', 'hidden')
        .style('font-weight', 'bold')
        .style('text-color', 'white')
        .style('opacity', 0.75)

    const circle = g.append('circle')
        .attr('r', 0)
        .attr('fill', 'red')
        .attr('opacity', 0.5)
        .style('stroke', 'white')
        .style('pointer-events', 'none')

    const listeningRect = g.append('rect')
        .attr('width', wG + '%')
        .attr('height', hG + '%')
        .attr('opacity', 0)
        .attr('z-index', 1);
        

    useEffect(() => {
        if (!payload || !selectedOptions || !startDate || !endDate) return; // wait until all are set  
        
        setStatName(payload.statName)
        setStartDate(dateParse(payload.startDate))
        setEndDate(dateParse(payload.endDate))
        setData(filterData(payload.dataByFeature, selectedOptions)) // must be filtered

        if (!statName || !startDate || !endDate || !data) return;

        for (const featureKey in data) {
            const featureData = data[featureKey]
            
            const dates = getDateList(startDate, endDate);

            const chartData = createChartData(featureData, dates); // combine

            if (chartData.length == 0) return;

            const xRange = d3.extent(dates) as Date[]; // TODO: otherwise may be undefined
            const yMax = d3.max(featureData) as number;
            const yMin = d3.min(featureData) as number;

            const xScale = d3.scaleTime()
                .range([0, wG])
                .domain(xRange)
            const yScale = d3.scaleLinear()
                .range([hG, 0])
                .domain([yMin - 25, yMax - 25]) 

            g.append('g')
                .attr('transform', `translate(0,${hG})`)
                .call(d3.axisBottom(xScale)
                    .ticks(d3.timeMonth.every(1)))
            g.append('g')
                .call(d3.axisLeft(yScale))

            const line: any = d3.line()
                .x((d: any) => xScale(d.date))
                .y((d: any) => yScale(d.value))
            
            g.append('path')
                .datum(chartData)
                .attr('fill', 'none')
                .attr('stroke', 'steelblue')
                .attr('stroke-width', 2)
                .attr('d', line)

            listeningRect.on('mousemove', (e: any) => {
                const [xCoord] = d3.pointer(e)
                const bisectDate = d3.bisector((d: DataPoint) => d.date).left

                const x0: any = xScale.invert(xCoord);
                const i = bisectDate(chartData, x0, 1);
                const d0: any = chartData[i]
                const d1: any = chartData[i-1]
                const d: DataPoint = x0 - d0.date > d1.date - x0 ? d1 : d0;
                const xPos = xScale(d.date);
                const yPos = yScale(d.value)

                circle
                    .attr('cx', xPos)
                    .attr('cy', yPos)
                    .transition()
                    .duration(50)
                    .attr('r', 2)
                
                tooltip
                    .style('display', 'block')
                    .style('left', `${xPos}px`)
                    .style('top', `${yPos}px`)
                    .style('visibility', 'visible')
                    .text(`${d.value} on ${d.date.toLocaleDateString()}`)
            })
        }
    }, [selectedOptions]);

    return (
        <>
            <h1 className="text-[24px] my-5">Chart</h1>
            <div id='chart-container' className='relative'>
                <svg ref={svgRef}/>
            </div>

        </>
    )
}