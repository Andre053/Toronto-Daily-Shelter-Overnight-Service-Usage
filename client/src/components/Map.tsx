import { useEffect, useRef, useState } from "react";
import { geoPath } from "d3";
import { FeatureCollection } from "geojson";
import '../app/globals.css';
import { GeoData, ServiceUserDataAll } from "@/types/Data";
import * as d3 from "d3";

import { getFilterData } from "./ExploreOptions";

// display the heatmap legend
function ColourLegend({lowColour, highColour, maxVal, minVal}: {lowColour: string, highColour: string, maxVal: number, minVal: number}) {
    const x = 20
    const y = 20

    const divClass = `m-3 flex align-center absolute z-2 top-${x} left-${y} w-40 bg-gray-100 border-black border-2`
    //const legendClass = `w-20 h-50 bg-gradient-to-b from-${highColour} to-${lowColour} text-white`
    const legendClass = `w-40 bg-gradient-to-r from-yellow-400 to-red-500 border-l-1 border-r-1 border-black`

    return (
        <div className={divClass} >
            <span className="w-15 text-center p-1">{minVal}</span>
            <div
                className={legendClass}
            />
            <span className="w-15 text-center p-1">{maxVal}</span>
        </div>
    )
} 

// takes geoJson data from backend, keeps track of whether map is generated with FSA or neighbourhood data
// calls all related map components to display on the page
// manages all key state variables
// TODO: Layer both geomaps? Neighbourhood layer could be used to display the data for the user
type GeoMapProps = {
    width: number;
    height: number;
    geoData: GeoData;
    setSelectedArea: any;
    filterData: any;
    setFilterData: any;
}

export function GeoMap({ width, height, geoData, filterData, setFilterData, setSelectedArea}: GeoMapProps) {
    const featureCollection: FeatureCollection = geoData.featureCollection
    
    const [zoomTransform, setZoomTransform] = useState(null);
        
    const projection = d3.geoMercator()
        .fitSize([width/1.75, height/2.25], featureCollection);

    const geoGenerator = geoPath().projection(projection);

    const svgRef = useRef<SVGSVGElement | null>(null);
    const gRef = useRef<SVGGElement | null>(null);

    const zoom: any = d3.zoom()
        .scaleExtent([1, 2]) // TODO: Get best scale extent
        .on("zoom", (e) => { 
            setZoomTransform(e.transform)
        });
    const mouseOverPath = (e: any) => {
        d3.selectAll('path')
            .transition()
            .duration(200)
            .style('opacity', .5)
        d3.select(e.target)
            .transition()
            .duration(200)
            .style('opacity', 0.8)
            .style('stroke', 'black')
        d3.select('#tooltip-div')
            .text(e.target.attributes[0].value)
    };
    const mouseLeavePath = (e: any) => {
        d3.selectAll('path')
            .transition()
            .duration(200)
            .style('opacity', .6)
        d3.select(e.target)
            .transition()
            .duration(200)
    };
    const mouseClickPath = (e: any) => {
        const area = e.target.attributes[0].value
        setSelectedArea(area)

        // TODO: Keep the target selected on the map once clicked, until a new one is clicked
        // if opacity is 1, leave it 
        d3.select(e.target)
            .transition()
            .duration(200)
            .style('opacity', .6)
            .attr('fill', 'green') // TODO: remove colour and ID, set to old colour
            .attr('id', 'fsa-selected') // sets to selected
    };
    const mouseOutPath = (e: any) => {
        d3.select('path')
            .style('opacity', 0.2)
            .style('stroke', 'black')
    };
    const mouseOverG = (e: any) => {
        d3.select('#tooltip-div')
            .style('visibility', 'visible');
    };
    const mouseMoveG = (e: any) => {
        d3.select('#tooltip-div')
            .style('top', (e.clientY-20)+'px') // get position on entire page
            .style('left', (e.clientX+5)+'px');
    };
    const mouseOutG = (e: any) => {
        d3.select('#tooltip-div')
            .style('visibility', 'hidden');
    };
    useEffect(() => {
        console.log('[Map.tsx] useEffect called with width', width, 'height', height)
        if (!geoData || !width || !height) return;
        
        const svg = d3.select(svgRef.current)
            .style('position', 'relative');
        const g = d3.select(gRef.current)
            .attr('id', 'map-group')
            .style('position', 'relative')
            .style('visibility', 'hidden');

        svg.node()?.addEventListener('wheel', (e) => {
            e.preventDefault()
        }, { passive: false });

        svg
            .attr('width', width/1.5)
            .attr('height', height/2)
            .call(zoom);

        // add the tooltip div 
        // where the div is appended matters
        // the SVG element does not know how to handle a div
        d3.select('body') 
            .append('div')
            .attr('id', 'tooltip-div')
            .style('position', 'absolute')
            .style('visibility', 'hidden')
            .style('font-weight', 'bold')
            .style('text-color', 'white')
            .text('test')

        g.selectAll('*').remove(); // remove all path elements when geodata changed

        // add tooltip functionality
        g.on('mouseover', mouseOverG)
            .on('mousemove', mouseMoveG)
            .on('mouseout', mouseOutG);

        g.selectAll('path')
            .data(featureCollection.features)
            .enter()
            .append('path')
                .attr('key', (d) => d.properties?.CFSAUID)
                .attr('d', geoGenerator)
                .attr('fill', 'gray') // have original map be white? gray?
                .on('mouseover', mouseOverPath)
                .on('mouseleave', mouseLeavePath)
                .on('click', mouseClickPath)
                .on('mouseout', mouseOutPath)

        if (!filterData) getFilterData('serviceUsers', setFilterData); // should trigger the recolour
     }, [geoData, width, height]);

     useEffect(() => {
        const g = d3.select(gRef.current);
        g.attr('transform', zoomTransform);
     }, [zoomTransform])

    // TODO: Improve spacing of info elements
    // TODO: Add colour legend when fixed
    // ColourLegend lowColour={'#ebc034'} highColour={'#eb4034'} maxVal={fsaStats.max} minVal={0}/>
    const styles = `justify-center z-1 grid col-span-1`
    return (
        <>
            <div id='map-container' className={styles}>
                <div className='relative'>
                    <svg ref={svgRef}>
                        <g ref={gRef} />
                    </svg>
                </div>
            </div>
        </>
    )
}