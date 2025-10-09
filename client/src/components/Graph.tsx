'use client'
import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { DataPoint, GraphData} from "@/types/Data";
import { useState } from "react";

type Props = {
    data: GraphData | null;
}
export function LineChart({data}: Props) {
    // pixels
    const wSVG = 600;
    const hSVG = 500;

    const svgRef = useRef<SVGSVGElement | null>(null);
    const gRef = useRef<SVGGElement | null>(null);
    const tooltipRef = useRef<any | null>(null)
    const margin = { top: 30, right: 40, bottom: 40, left: 100}
    const wG = wSVG-margin.left-margin.right 
    const hG = hSVG-margin.top-margin.bottom

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
            .attr('transform', `translate(${margin.left}, ${margin.top})`)

        g.selectAll('*').remove()

        const circle = g.append('circle')
            .attr('r', 0)
            .attr('fill', 'red')
            .attr('opacity', 0.5)
            .style('stroke', 'white')
            .style('pointer-events', 'none');

        const listeningRect = g.append('rect')
            .attr('width', wG + 'px')
            .attr('height', hG + 'px')
            .attr('opacity', 0)
            .attr('z-index', 1);

        const tooltip = d3.select(tooltipRef.current)
            .attr('id', 'tooltip-chart')
            .style('position', 'absolute')
            .style('visibility', 'hidden')
            .style('font-weight', 'bold')
            .style('text-color', 'white')
            .style('opacity', 0.75);

        const xScale = d3.scaleTime()
            .range([0, wG])
            .domain(dates)
        const yScale = d3.scaleLinear()
            .range([hG, 0])
            .domain([0, yMax + 25]) 

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr("x", wSVG/2)
            .attr('y', hSVG)
            .text("Date")
        svg.append("text")
            .attr("text-anchor", "end")
            .attr("y", 1)
            .attr("x", -hSVG/2)
            .attr("dy", "1.5em")
            .attr("transform", "rotate(-90)")
            .text("Statistic"); // get title from backend
        let ticks = d3.timeMonth.every(6)
        //if (data.timespan == 'yearly')  ticks = d3.timeYear.every(1)
        //else if (data.timespan == 'monthly')  ticks = d3.timeMonth.every(3)

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
        // add back listeningOn
        listeningRect.on('mousemove', (e: any) => {
            const [xCoord] = d3.pointer(e)
            const bisectDate = d3.bisector((d: DataPoint) => d.DATE).left

            const x0: any = xScale.invert(xCoord);
            const i = bisectDate(dataPoints, x0, 1);
            const d0: any = dataPoints[i]
            const d1: any = dataPoints[i-1]
            const d: DataPoint = x0 - d0.DATE > d1.DATE - x0 ? d1 : d0;
            const xPos = xScale(d.DATE);
            const yPos = yScale(d.STAT);

            circle
                .attr('cx', xPos)
                .attr('cy', yPos)
                .transition()
                .duration(50)
                .attr('r', 5)
            tooltip
                .style('display', 'block')
                .style('left', `${xPos}px`)
                .style('top', `${yPos}px`)
                .style('visibility', 'visible')
                .text(`${d.STAT} on ${d.DATE.toLocaleDateString()}`)
        })
        
    }, [data]);


    /**
     * 
     */

    return (
        <div className="flex text-center justify-right items-right">
            <h1 className="text-4xl my-5">Statistic over time</h1>
            <div id='chart-container' className='relative'>
                <svg ref={svgRef}>
                    <g ref={gRef}>
                    </g>
                </svg>
                <div ref={tooltipRef} />
            </div>
        </div>
    )
}