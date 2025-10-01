'use client'

import { useEffect, useRef, useState } from "react";
import { geoPath } from "d3";
import { FeatureCollection } from "geojson";
import '../app/globals.css';
import { GeoData, FsaData, AreaData } from "@/types/Data";
import * as d3 from "d3";
import dayjs from "dayjs";
import { MapOptions } from "./MapOptions";
import { MapData } from "./MapData";
import { DatePickers } from "./DataPicker";

/*
    Map.tsx
    - Contains the main map component with styling for hovering
    - Uses GeoJson data of FSA codes or neighbourhoods within Toronto
        - Neighbourhoods functionality is lacking due to no related feature in the backend dataset
    - Colourlegend is in progress
*/

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
// TODO: Add heatmap functionality with selectedMapFilter
// TODO: Layer both geomaps? Neighbourhood layer could be used to display the data for the user
function GeoMap({ geoData, isFsa, setIsFsa}: {geoData: GeoData, isFsa: any, setIsFsa: any}) {

    const featureCollection: FeatureCollection = geoData.featureCollection

    const [selectedArea, setSelectedArea] = useState('')
    const [selectedMapFilter, setSelectedMapFilter] = useState('')
    const [zoomTransform, setZoomTransform] = useState(null);
    const [startDate, setStartDate] = useState(dayjs('2025-01-01'))
    const [endDate, setEndDate] = useState(dayjs())

    const parentHeight = 900 // TODO: want to set dynamically, sometimes window.innerHeight is null
    const height = parentHeight / 1.5 as number
    const width = height
        
    const projection = d3.geoMercator()
        .fitSize([width, height], featureCollection)

    const geoGenerator = geoPath().projection(projection)

    const svgRef = useRef<SVGSVGElement | null>(null)
    const gRef = useRef<SVGGElement | null>(null)

    const zoom: any = d3.zoom()
        .scaleExtent([1, 10000])
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
            .style('opacity', 1)
            .style('stroke', 'black')
    }

    const mouseLeave = (e: any) => {
        d3.selectAll('path')
            .transition()
            .duration(200)
            .style('opacity', .6)
        d3.select(e.target)
            .transition()
            .duration(200)
    }

    const mouseClick = (e: any) => {
        const area = isFsa ? e.target.attributes[0].value : e.target.attributes[0].value
        console.log("Selected area")
        setSelectedArea(area)

        // TODO: Keep the target selected on the map once clicked, until a new one is clicked
        d3.select(e.target)
            .transition()
            .style('opacity', 1)
            .style('stroke', 'black')
    }

    useEffect(() => {
        if (!geoData) return;
        
        const svg = d3.select(svgRef.current)
        const g = d3.select(gRef.current);

        g.selectAll('*').remove() // remove all path elements when geodata changed

        // prevent wheel from scrolling the page when on SVG element
        svg.node()?.addEventListener('wheel', (e) => {
            e.preventDefault()
        }, { passive: false })

        svg
            .attr('width', width)
            .attr('height', height)
            .call(zoom);

        g.attr('transform', zoomTransform);
        
        if (isFsa) {
            g.selectAll('path')
            .data(featureCollection.features)
            .enter()
            .append('path')
                .attr('key', (d) => d.properties?.CFSAUID)
                .attr('d', geoGenerator)
                .classed('stroke-black fill-orange-400', true)
                .on('mouseover', mouseOver)
                .on('mouseleave', mouseLeave)
                .on('click', mouseClick)
        } else {
            g.selectAll('path')
            .data(featureCollection.features)
            .enter()
            .append('path')
                .attr('key', (d) => d.properties?.AREA_NAME)
                .attr('d', geoGenerator)
                .classed('stroke-black fill-green-400', true)
                .on('mouseover', mouseOver)
                .on('mouseleave', mouseLeave)
                .on('click', mouseClick)
        }
     }, [geoData, zoomTransform, isFsa])

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
            <div className='grid grid-cols-1 content-start gap-4 border-4 bg-gray-200 p-5'>
                <MapOptions mapFilter={selectedMapFilter} setMapFilter={setSelectedMapFilter} isFsa={isFsa} setIsFsa={setIsFsa} /><br/>
                <DatePickers startDate={startDate} endDate={endDate} setStartDate={setStartDate} setEndDate={setEndDate}/><br/>
                <MapData area={selectedArea} isFsa={isFsa} />
            </div>
        </>
    )
}

type Props = {
    initialGeoData: GeoData;
}

export function Map({ initialGeoData }: Props) {
    const [isFsa, setIsFsa] = useState(initialGeoData.name === 'toronto_fsa_codes_generated')
    const [geoData, setGeoData] = useState(initialGeoData)

    useEffect(() => {
        const url = isFsa ? "http://localhost:8080/geodata/fsa" : "http://localhost:8080/geodata/neighbourhood"
        const fc = async () => {
            const data = await fetch(url)
                .then((res) => res.json())
                .then((servData) => servData.data)
            setGeoData({
                name: data.name,
                featureCollection: data
            })
        } 
        fc()     
    }, [isFsa])

    return (
        <>
            <h1 className="text-[36px] mb-4 mt-4">Map of Toronto {isFsa ? 'by FSA' : 'by Neighbourhood'}</h1>
            <div id='geomap-container' className='grid content-center grid-cols-2 gap-5 ml-10 mr-10'>
                <GeoMap geoData={geoData} isFsa={isFsa} setIsFsa={setIsFsa} />
            </div>
            
        </>
    )
}