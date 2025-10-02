import { useEffect, useRef } from "react";
import * as d3 from "d3";
import { ServiceUserDataAll } from "@/types/Data";
/* 
    Chart.tsx
    - Not currently implemented
    - Use to show charts such as:
        - Histograms of data like service users, separated by features such as FSA, neighbourhood, shelter, organization, etc. 
        - Line graphs of data like service users over time, fitlered by features such as FSA, program type, 
        - Pie charts of data like 
*/

type Props = {
    allData: ServiceUserDataAll;
    width: number;
    height: number;
}

export function LineChart({ allData, width, height }: Props) {
    const svgRef = useRef<SVGSVGElement | null>(null);
    const gRef = useRef<SVGGElement | null>(null);

    useEffect(() => {
        if (!allData || !width || !height) return; // wait until all are set
        console.log(`Within line chart, width ${width}, height ${height}`)

        // data to use
        const data = allData['M5V']['daily_stats']

        const svg = d3.select(svgRef.current)
        
        svg
            .attr('width', width/1.5)
            .attr('height', height/2)

        // want multiple g elements for each part
        const gBody = svg.append('g') // body of the page
        gBody.attr('transform', `translate(${40}, ${40})`)

        const gX = svg.append('g') // x axis
        const gY = svg.append('g') // y axis

        // set the scales for each

        // set the data
        svg.append('path')
            .data()

    }, [allData, width, height])
    return (
        <>
            <svg ref={svgRef}>
            </svg>
        </>
    )
}