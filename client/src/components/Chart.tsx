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

type Props = {
    data: any
}

type HistoProps = {
    data: {value: number }[];
    width?: number;
    height?: number;
    marginTop?: number;
    marginRight?: number;
    marginBottom?: number;
    marginLeft?: number;
}

function HistoChart({
    data,
    width = 960,
    height = 500,
    marginTop = 20,
    marginRight = 20,
    marginBottom = 30,
    marginLeft = 40
}: HistoProps) {

    // TODO: Review useRef
    const svgRef = useRef<SVGSVGElement | null>(null)

    useEffect(() => {
        if (!data || data.length === 0) return;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove(); // TODO: Review this?

        const g = svg
            .append('g')
            .attr('transform', `translate(${marginLeft},${marginTop})`);
        
        const values = data.map((d) => d.value)

        const x = d3
            .scaleLinear()
            .domain(d3.extent(values) as [number, number])
            .nice()
            .range([0, innerWidth])
        
            const bins = d3
                .bin()
                .domain(x.domain() as [number, number])
                .thresholds(20)(values); // 20 bins
            
            const y = d3
                .scaleLinear()
                .domain([0, d3.max(bins, (d) => d.length) as number])
                .nice()
                .range([innerHeight, 0]);
            
            g.append('g')
                .attr('transform', `translate(0,${innerHeight})`)
                .call(d3.axisBottom(x))

            g.append('g').call(d3.axisLeft(y));

            g.selectAll('rect')
                .data(bins)
                .join('rect')
                .attr('x', d => x(d.x0!))
                .attr('y', d => y(d.length))
                .attr('width', d => x(d.x1!) - x(d.x0!) -1)
                .attr('height', d => innerHeight - y(d.length))
                .attr('fill', 'green')
    }, [data])

    return (
        <>
            <h1 className="text-[36px]">Charts</h1>
            <div className='grid content-start grid-cols-3 gap-4'>
                <div className='grid col-span-2'>
                </div>
                <div className='grid'>
                    <h2>Data to show</h2>
                </div>
                <svg ref={svgRef} width={width} height={height}/>
                
            </div>
            
        </>
    );
}