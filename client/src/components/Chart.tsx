import { useEffect, useRef } from "react";
import * as d3 from "d3";

/* 
    Chart.tsx
    - Not currently implemented
    - Use to show charts such as:
        - Histograms of data like service users, separated by features such as FSA, neighbourhood, shelter, organization, etc. 
        - Line graphs of data like service users over time, fitlered by features such as FSA, program type, 
        - Pie charts of data like 
*/

export function lineChart() {
    const svgRef = useRef<SVGSVGElement | null>(null);
    const gRef = useRef<SVGGElement | null>(null);

    useEffect(() => {
        const svg = d3.select(svgRef.current)

        const g = svg.append('g')

    })
    return (
        <>
            <svg ref={svgRef}>
            </svg>
        </>
    )
}