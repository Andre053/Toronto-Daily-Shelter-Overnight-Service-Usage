import { useEffect, useRef, useState } from "react";
import { geoPath } from "d3";
import { FeatureCollection } from "geojson";
import '../app/globals.css';
import { GeoData, ServiceUserDataAll } from "@/types/Data";
import * as d3 from "d3";

import { getFilterData } from "./MapOptions";

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
    isFsa: any;
    setSelectedArea: any;
    setMapGenerated: any;
    filterData: any;
    setFilterData: any;
}

export function GeoMap({ width, height, geoData, filterData, setFilterData, isFsa, setSelectedArea, setMapGenerated}: GeoMapProps) {
    const featureCollection: FeatureCollection = geoData.featureCollection
    
    const [zoomTransform, setZoomTransform] = useState(null);
    
        
    const projection = d3.geoMercator()
        .fitSize([width, height], featureCollection);

    const geoGenerator = geoPath().projection(projection);

    const svgRef = useRef<SVGSVGElement | null>(null);
    const gRef = useRef<SVGGElement | null>(null);

    const zoom: any = d3.zoom()
        .scaleExtent([1, 2]) // TODO: Get best scale extent
        .on("zoom", (e) => { 
            setZoomTransform(e.transform)
        });

    const mouseOver = (e: any) => {
        d3.selectAll('path')
            .transition()
            .duration(200)
            .style('opacity', .5)

        d3.select(e.target)
            .transition()
            .duration(200)
            .style('opacity', 0.8)
            .style('stroke', 'black')
    };

    const mouseLeave = (e: any) => {
        d3.selectAll('path')
            .transition()
            .duration(200)
            .style('opacity', .6)
        d3.select(e.target)
            .transition()
            .duration(200)
    };

    const mouseClick = (e: any) => {
        const area = isFsa ? e.target.attributes[0].value : e.target.attributes[0].value
        console.log("[GeoMap] Selected area")
        setSelectedArea(area)

        // TODO: Keep the target selected on the map once clicked, until a new one is clicked
        // if opacity is 1, leave it 
        d3.select(e.target)
            .style('opacity', 1)
            .style('stroke', 'black')
    };

    useEffect(() => {
        if (!geoData) return;
        
        const svg = d3.select(svgRef.current);
        const g = d3.select(gRef.current);

        g.selectAll('*').remove(); // remove all path elements when geodata changed

        // prevent wheel from scrolling the page when on SVG element
        svg.node()?.addEventListener('wheel', (e) => {
            e.preventDefault()
        }, { passive: false });

        svg
            .attr('width', width)
            .attr('height', height)
            .call(zoom);
        
        if (isFsa) {
            g.selectAll('path')
                .data(featureCollection.features)
                .enter()
                .append('path')
                    .attr('key', (d) => d.properties?.CFSAUID)
                    .attr('d', geoGenerator)
                    .attr('fill', 'green')
                    .on('mouseover', mouseOver)
                    .on('mouseleave', mouseLeave)
                    .on('click', mouseClick);
            setMapGenerated(true) // supposed to trigger the colouring of the elements
        } else {
            // use to add an additional layer
            g.selectAll('path')
                .data(featureCollection.features)
                .enter()
                .append('path')
                    .attr('key', (d) => d.properties?.AREA_NAME)
                    .attr('d', geoGenerator)
                    .on('mouseover', mouseOver)
                    .on('mouseleave', mouseLeave)
                    .on('click', mouseClick);
        }
        if (!filterData) getFilterData('serviceUsers', setFilterData)
     }, [geoData, isFsa]);

     useEffect(() => {
        const g = d3.select(gRef.current);
        g.attr('transform', zoomTransform);

     }, [zoomTransform])

    // TODO: Improve spacing of info elements
    // TODO: Add colour legend when fixed
    // ColourLegend lowColour={'#ebc034'} highColour={'#eb4034'} maxVal={fsaStats.max} minVal={0}/>
    return (
        <>
            <div id='map-container' className='justify-center z-1 grid col-span-1'>
                <div className='relative'>
                    <svg ref={svgRef} className='border-3 border-gray-800 bg-gray-200'>
                        <g ref={gRef} />
                        
                    </svg>
                </div>
            </div>
            
        </>
    )
}