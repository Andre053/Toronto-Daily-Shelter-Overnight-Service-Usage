import { useEffect, useInsertionEffect, useRef, useState } from "react";
import { geoPath } from "d3";
import { FeatureCollection } from "geojson";
import '../app/globals.css';
import { GeoData } from "@/types/Data";
import * as d3 from "d3";

// takes geoJson data from backend, keeps track of whether map is generated with FSA or neighbourhood data
// calls all related map components to display on the page
// manages all key state variables
// TODO: Layer both geomaps? Neighbourhood layer could be used to display the data for the user

type PropsMap = {
    width: number;
    height: number;
    geoData: GeoData;
    setSelectedArea: any;
}

export function MapFsa({width, height, geoData, setSelectedArea}: PropsMap) {
    const featureCollection: FeatureCollection = geoData.featureCollection
    
    const [selectedPath, setSelectedPath] = useState<any>(null); // TODO: Keep track of the selected FSA for colouring
    const [zoomTransform, setZoomTransform] = useState(null);
        
    const projection = d3.geoMercator()
        .fitSize([width/1.5, height/2], featureCollection);

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
            .style('opacity', .8)
        d3.select(e.target)
            .transition()
            .duration(200)
            .style('opacity', 1)
            .style('stroke', 'black')
        d3.select('#tooltip-div')
            .text(e.target.attributes[0].value)
    };
    const mouseLeavePath = (e: any) => {
        d3.selectAll('path')
            .transition()
            .duration(200)
            .style('opacity', 1)
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
            .duration(800)
            .style('opacity', 1)
            .style('stroke', 'green')
            .attr('id', 'fsa-selected') // sets to selected
    };
    // does nothing
    const mouseOutPath = (e: any) => {
        d3.selectAll('path') 
            .style('stroke', 'black')
    };
    const mouseOverG = (e: any) => {
        d3.select('#tooltip-div')
            .style('visibility', 'visible');
    };
    const mouseMoveG = (e: any) => {
        d3.select('#tooltip-div')
            .style('top', (e.clientY-25)+'px') // get position on entire page
            .style('left', (e.clientX+10)+'px');
    };
    const mouseOutG = (e: any) => {
        d3.select('#tooltip-div')
            .style('visibility', 'hidden');
    };
    useEffect(() => {
        if (!geoData || !width || !height) return;
        
        const svg = d3.select(svgRef.current)
            .style('position', 'relative');
            
        const g = d3.select(gRef.current)
            .attr('id', 'map-group')
            .style('position', 'relative')
            //.style('visibility', 'hidden'); // hidden until colours set

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
            .style('background-color', 'white')
            .style('padding', '1px')
            .style('color', 'black')
            .style('border', 'solid')
            .style('z-index', 2)

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
                .attr('fill', 'lightgray') // have original map be white? gray?
                .style('stroke', 'black')
                .on('mouseover', mouseOverPath)
                .on('mouseleave', mouseLeavePath)
                .on('click', mouseClickPath)
                .on('mouseout', mouseOutPath)

     }, [geoData, width, height]);

     useEffect(() => {
        const g = d3.select(gRef.current);
        g.attr('transform', zoomTransform);
     }, [zoomTransform])

    // TODO: Improve spacing of info elements
    // TODO: Add colour legend when fixed
    // ColourLegend lowColour={'#ebc034'} highColour={'#eb4034'} maxVal={fsaStats.max} minVal={0}/>
    const styles = `relative justify-center z-1 grid col-span-1`
    return (
        <>
            <h1 className="text-2xl my-3 text-center">Toronto by Forward Sortation Addresses</h1>
            <div id='map-container' className={styles}>
                <svg ref={svgRef} className="border border-5 border-gray-500 rounded-3xl m-2">
                    <g ref={gRef} />
                </svg>
            </div>
        </>
    )
}