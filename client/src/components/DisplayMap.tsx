import { useEffect, useInsertionEffect, useRef, useState } from "react";
import { geoPath } from "d3";
import { FeatureCollection } from "geojson";
import '../app/globals.css';
import { ServerData, GeoData, Stats, StatByFsa, MonthlyStatsFsa, AllStatsFsa, StatsKey } from "@/types/Data";
import * as d3 from "d3";

// takes geoJson data from backend, keeps track of whether map is generated with FSA or neighbourhood data
// calls all related map components to display on the page
// manages all key state variables
// TODO: Layer both geomaps? Neighbourhood layer could be used to display the data for the user

type HeatmapData = {
    statName: StatsKey;
    statMax: number;
    statMin: number
    stats: StatByFsa;
}
async function getOverallStats(setOverallStats: any) {
  await fetch('http://localhost:8080/data/all/all')
        .then(res => res.json())
        .then((resJson: ServerData) => {
            const data: AllStatsFsa = resJson.data
            setOverallStats(data.STATS)
        })
}
const getColour = (colourStart: string, colourEnd: string, value: number, max: number, min: number) => {
    const colourScale = d3.scaleLinear([min, max], [colourStart, colourEnd])
    return colourScale(value)
}
const setPathColour = (data: HeatmapData) => {
    const g = d3.select('#map-group'); // should only be a single g tag

    g.selectAll('path') // go through all paths and change the colour
        .classed('stroke-black', true)
        .attr('fill', (d: any) => {
            const fsa: string = d.properties.CFSAUID;
            const fsaData = data.stats[fsa];
            if (fsaData) return getColour('#fdbb84', '#e34a33', fsaData, data.statMax, data.statMin);
            return 'gray';
        })
    g.style('visibility', 'visible') // make visible once recoloured
}
const getHeatmapData = (stat: StatsKey, mapData: AllStatsFsa[]): HeatmapData => {
    const heatmapData: HeatmapData = {
        statName: stat,
        statMax: 0,
        statMin: 10000,
        stats: {}
    }
    const statByFsa: StatByFsa = {}
    mapData.forEach(v => {
            const curStat = v.STATS[stat]
            statByFsa[v.FSA] = curStat; // TODO: Type error, fix
            if (heatmapData.statMax < curStat) heatmapData.statMax = curStat;
            if (heatmapData.statMin > curStat) heatmapData.statMin = curStat;
        });

    heatmapData.stats = statByFsa;
    return heatmapData
}
type PropsSettings = {
    selectedArea: string | null;
    mapData: AllStatsFsa[];
}

/**
 * 1. Show the map with the overall map data
 * 2. Show basic stats for the time
 * 3. Allow selecting a specific FSA, obtain specific stats for it
 */
export function MapSettings({selectedArea, mapData}: PropsSettings) {
    const [selectedAreaData, setSelectedAreaData] = useState<AllStatsFsa | null>(null);
    const [selectedHeatmapOption, setSelectedHeatmapOption] = useState<StatsKey>('MEAN_SERVICE_USERS')
    const [heatmapData, setHeatmapData] = useState<HeatmapData | null>(null); 
    const [overallStats, setOverallStats] = useState<Stats | null>(null);

    const currentDate = new Date(); // TODO: Not using EST
    const maxDate = new Date(currentDate.setDate(currentDate.getDate() - 1))

    const onChange = (e: any) => {
        setSelectedHeatmapOption(e.target.value)
        setHeatmapData(null)
        console.log('Set selected heatmap option to', e.target.value)
    }

    useEffect(() => {
        getOverallStats(setOverallStats);
    }, [])

    useEffect(() => {
        // null on first call
        if (!selectedArea) return;
        // mapData has all FSAs, simply select the FSA 
        let set = false;
        mapData.forEach(v => {
            if (v.FSA == selectedArea) { 
                setSelectedAreaData(v);
                set = true;
            };
        });
        if (!set) setSelectedAreaData(null);
    }, [selectedArea]);
    
    useEffect(() => { // should run on first time, colouring the map, then run on subsequent when changing
        // heat map data is within the mapData
        console.log('Checking heatmap with data', heatmapData)

        if (!heatmapData) {
            setHeatmapData(getHeatmapData(selectedHeatmapOption, mapData))
        } else {
            setPathColour(heatmapData)
        }
    }, [selectedHeatmapOption, heatmapData]);
    return (
        <>
            <h1 className="text-3xl">Info and options</h1>
            <div className="ml-5">
                <h1 className="text-2xl py-2">Heatmap statistic</h1>
                <select 
                    id="selected-info"
                    name="selectedInfo" 
                    className="p-1 border-black border-2"
                    onChange={onChange}
                >
                    <option value="MEAN_SERVICE_USERS">Service users</option>
                    <option value="MEAN_OCCUPIED_BEDS">Occupied beds</option>
                    <option value="MEAN_UNOCCUPIED_BEDS">Unoccupied beds</option>
                    <option value="MEAN_OCCUPIED_ROOMS">Occupied rooms</option>
                    <option value="MEAN_UNOCCUPIED_ROOMS">Unoccupied rooms</option>
                    <option value="UNIQUE_ORG_COUNT">Active organizations</option>
                    <option value="UNIQUE_PROGRAM_COUNT">Active programs</option>
                    <option value="UNIQUE_LOCATION_COUNT">Active shelters</option>
                </select>
                <h1 className="text-2xl py-2">Date range</h1>
                <input className="border" type="date" id="start-date" value="2021-01-01" min="2021-01-01" max={maxDate.toISOString().split('T')[0]}/>
                <input className="border"type="date" id="end-date" value={maxDate.toISOString().split('T')[0]} min="2021-01-01" max={maxDate.toISOString().split('T')[0]}/>
                {overallStats && (
                    <>
                        <h1 className="text-2xl p-2">Map statistics</h1>
                        <ul className='list-disc text-left'>
                            <li>There are {overallStats.MEAN_SERVICE_USERS} average service users across the city each day</li>
                            <li>Every day there are on average {overallStats.UNIQUE_SHELTER_COUNT} active shelters, {overallStats.UNIQUE_ORG_COUNT} active organizations,<br/> and {overallStats.UNIQUE_PROGRAM_COUNT} active programs on average</li>
                            <li>Programs providing beds have {overallStats.MEAN_OCCUPIED_BEDS} occupied, {overallStats.MAX_UNOCCUPIED_BEDS} unoccupied on average</li>
                            <li>Programs providing rooms have {overallStats.MAX_OCCUPIED_ROOMS} occupied, {overallStats.MAX_UNOCCUPIED_ROOMS} unoccupied on average</li>
                            <li>The most service users supported in one day was {overallStats.MAX_SERVICE_USERS}</li>
                        </ul>
                    </>
                    
                )}
                <h1 className="text-xl p-2">{selectedArea ? `FSA selected: ${selectedArea}` : 'No FSA selected'}</h1>
                <div className="">
                    {selectedArea ? ((selectedAreaData) ? (Object.keys(selectedAreaData).length !== 0) ? (
                        <>
                            <ul className='list-disc text-left'>
                                {selectedAreaData.STATS.MEAN_SERVICE_USERS !== 0 && <li>{selectedAreaData.STATS.MEAN_SERVICE_USERS} average service users per day</li>}
                                {selectedAreaData.STATS.MEAN_OCCUPIED_BEDS !== 0 &&<li>{selectedAreaData.STATS.MEAN_OCCUPIED_BEDS} average occupied beds per day</li>}
                                {selectedAreaData.STATS.MEAN_UNOCCUPIED_BEDS !== 0 &&<li>{selectedAreaData.STATS.MEAN_UNOCCUPIED_BEDS} average unoccupied beds per day</li>}
                                {selectedAreaData.STATS.MEAN_OCCUPIED_ROOMS !== 0 &&<li>{selectedAreaData.STATS.MEAN_OCCUPIED_ROOMS} average occupied rooms per day</li>}
                                {selectedAreaData.STATS.MEAN_UNOCCUPIED_ROOMS !== 0 &&<li>{selectedAreaData.STATS.MEAN_UNOCCUPIED_ROOMS} average unoccupied rooms per day</li>}
                                {selectedAreaData.STATS.UNIQUE_PROGRAM_COUNT !== 0 &&<li>{selectedAreaData.STATS.UNIQUE_PROGRAM_COUNT} active programs</li>}
                                {selectedAreaData.STATS.UNIQUE_ORG_COUNT !== 0 &&<li>{selectedAreaData.STATS.UNIQUE_ORG_COUNT} active organizations</li>}
                                {selectedAreaData.STATS.UNIQUE_SHELTER_COUNT !== 0 &&<li>{selectedAreaData.STATS.UNIQUE_SHELTER_COUNT} active shelters</li>}
                            </ul>
                        </>
                    ) : (<>No data found...</>) : (<>Loading...</>)) : <>No selected area</>} 
                </div>
            </div>
            
        </>
    )
}

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
            <h1 className="text-3xl">Toronto by FSA</h1>
            <div id='map-container' className={styles}>
                <svg ref={svgRef} className="border m-2">
                    <g ref={gRef} />
                </svg>
            </div>
        </>
    )
}