'use client'
import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { DataPoint, GraphData} from "@/types/Data";
import { useState } from "react";


type statKey = {
    [key: string]: string;
}

const graphStatKey: statKey = {
    'SERVICE_USER_COUNT': 'Service Users',
    'OCCUPIED_BEDS': 'Occupied Beds',
    'UNOCCUPIED_BEDS': 'Unoccupied Beds',

}

const capitalize = (val: string) => {
    return String(val).charAt(0).toUpperCase() + String(val).slice(1)
}

const createTooltip = (tooltipId: string) => {
    return d3.select('body') 
        .append('div')
        .attr('id', tooltipId)
        .style('position', 'absolute')
        .style('visibility', 'hidden')
        .style('font-weight', 'bold')
        .style('background-color', 'white')
        .style('padding', '1px')
        .style('color', 'black')
        .style('border', 'solid')
        .style('z-index', 2)
        .style('opacity', 0.7)
}

// TODO: fix the type
const createCircle = (g: any, circleId: string) => {
    return g.append('circle')
        .attr('id', circleId)
        .attr('r', 0)
        .attr('fill', 'red')
        .attr('opacity', 0.5)
        .style('stroke', 'white')
        .style('pointer-events', 'none');
}

type Props = {
    data: GraphData | null;
}
export function LineChart({data}: Props) {
    // pixels
    const wSVG = 800;
    const hSVG = 500;

    const svgRef = useRef<SVGSVGElement | null>(null);
    const gRef = useRef<SVGGElement | null>(null);
    const tooltipRef = useRef<any | null>(null)
    const margin = { top: 30, right: 40, bottom: 40, left: 100}
    const wG = wSVG-margin.left-margin.right 
    const hG = hSVG-160

    useEffect(() => {
        if (!data) return; // wait until all are set  
        console.log('Drawing line chart', {data})
        const dataPoints: DataPoint[] = data.dataPoints
        dataPoints.forEach(dp => {
            dp.DATE = new Date(dp.DATE);
        })
            
        const yMax = data.max;
        const yMin = data.min;

        const dates = d3.extent(dataPoints, (d) => d.DATE)
        console.log({dates}, {dataPoints}, typeof(dataPoints[0].DATE))

        if (dates[0] == undefined) return;

        const svg = d3.select(svgRef.current)
            .attr('width', wSVG +'px')
            .attr('height', hSVG + 'px')
            .attr('border-weight', 'bold')

        const g = d3.select(gRef.current)
            .attr('transform', `translate(100, 100)`)
            //.attr('transform', `translate(${margin.left}, ${margin.top})`)

        g.selectAll('*').remove()

        const listeningRect = g.append('rect')
            .attr('id', 'listening-rect')
            .attr('width', wG + 'px')
            .attr('height', hG + 'px')
            .attr('opacity', 0)
            .attr('z-index', 1);

        const circle = createCircle(g, 'tooltip-circle')
        const circleMax = createCircle(g, 'tooltip-circle-max')
        const circleMin = createCircle(g, 'tooltip-circle-min')
        
        const tooltip =  createTooltip('tooltip-chart')
        const tooltipMax = createTooltip('tooltip-chart-max')
        const tooltipMin = createTooltip('tooltip-chart-min')

        const xScale = d3.scaleTime()
            .range([0, wG])
            .domain(dates)
        const yScale = d3.scaleLinear()
            .range([hG, 0])
            .domain([0, yMax + 25]) 


        svg.selectAll('text').remove()
        svg.append('text')
            .attr('text-anchor', 'end')
            .attr("x", wSVG/2+100)
            .attr('y', 50)
            .style('font-size', '24px')
            .text(`${capitalize(data.timespan)} ${graphStatKey[data.stat]}`)
        svg.append('text')
            .attr('text-anchor', 'end')
            .attr("x", wSVG/2)
            .attr('y', 475)
            .text("Date")
        svg.append("text")
            .attr("text-anchor", "end")
            .attr("y", 20)
            .attr("x", -hSVG/2)
            .attr("dy", "1.5em")
            .attr("transform", "rotate(-90)")
            .text("Statistic"); // get title from backend
        
        const ticks = d3.timeMonth.every(6)

        g.append('g')
            .attr('transform', `translate(0,${hG})`)
            .call(d3.axisBottom(xScale)
                .ticks(ticks))
        g.append('g')
            .call(d3.axisLeft(yScale))

        const line: any = d3.line()
            .x((d: any) => xScale(d.DATE))
            .y((d: any) => yScale(d.STAT))
        
        g.append('path')
            .datum(dataPoints)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 2)
            .attr('d', (d: any) => {
                console.log({d}); // the whole data?
                return line(d);
            })
        
        listeningRect.on('mousemove', (e: any) => {
            const [xCoord] = d3.pointer(e) // values relative to the element
            const bisectDate = d3.bisector((d: DataPoint) => d.DATE).left

            const x0: any = xScale.invert(xCoord);
            const i = bisectDate(dataPoints, x0, 1);
            const d0: any = dataPoints[i];
            const d1: any = dataPoints[i-1];
            const d: DataPoint = x0 - d0.DATE > d1.DATE - x0 ? d1 : d0;
            const xPos = xScale(d.DATE); 
            const yPos = yScale(d.STAT);

            circle
                .attr('cx', xPos)
                .attr('cy', yPos)
                .transition()
                .duration(50)
                .attr('r', 5);

            // tooltip needs abs value does not account for scroll
            const container = document.getElementById('listening-rect');
            if (!container) return;
            const containerDomRect = container.getBoundingClientRect();
            
            const xTooltip = xPos + containerDomRect.x
            const yTooltip = yPos + containerDomRect.y

            tooltip
                .style('left', `${xTooltip+10}px`)
                .style('top', `${yTooltip-30}px`)
                .text(`${d.DATE.toLocaleDateString()}: ${d.STAT}`);
        });
        listeningRect.on('mouseenter', () => {
            tooltip.style('visibility', 'visible')
            circle.style('visibility', 'visible')
        })
        listeningRect.on('mouseleave', () => {
            tooltip.style('visibility', 'hidden')
            circle.style('visibility', 'hidden')
        })
    }, [data]);

    return (
        <>
            <div id='chart-container' className='justify-center z-1 grid col-span-1'>
                <svg id='chart-svg' ref={svgRef} className="border border-5 border-gray-500 rounded-4xl ">
                    <g ref={gRef}>
                    </g>
                </svg>
            </div>            
        </>

    )
}