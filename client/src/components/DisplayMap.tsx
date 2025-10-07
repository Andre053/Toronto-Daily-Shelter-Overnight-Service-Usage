import { useEffect, useInsertionEffect, useRef, useState } from "react";
import { geoPath } from "d3";
import { FeatureCollection } from "geojson";
import '../app/globals.css';
import { DataByMonth, GeoData, DataCategory, StatByFsa } from "@/types/Data";
import * as d3 from "d3";

// takes geoJson data from backend, keeps track of whether map is generated with FSA or neighbourhood data
// calls all related map components to display on the page
// manages all key state variables
// TODO: Layer both geomaps? Neighbourhood layer could be used to display the data for the user

type Stats = {
    meanMonthlyUsers: number;
    meanMonthlyOccupiedBeds: number;
    meanMonthlyUnoccupiedBeds: number;
    meanMonthlyOccupiedRooms: number;
    meanMonthlyUnoccupiedRooms: number;
    meanMonthlyPrograms: number;
    meanMonthlyShelters: number;
    meanMonthlyOrgs: number;
    meanMonthlyLocations: number;
    maxMonthlyUsersFsa: string;
    maxMonthlyUsersMonth: string;
    maxMonthlyUsers: number;
    minMonthlyUsers: number;
}

const getColour = (colourStart: string, colourEnd: string, value: number, max: number, min: number) => {
    const colourScale = d3.scaleLinear([min, max], [colourStart, colourEnd])
    return colourScale(value)
}

const setPathColour = (statData: StatByFsa) => {
    const g = d3.select('#map-group'); // should only be a single g tag

    const values = Object.values(statData)
    const max = Math.max(...values);
    const min = Math.min(...values);

    g.selectAll('path') // go through all paths and change the colour
        .classed('stroke-black', true)
        .attr('fill', (d: any) => {
            const fsa: string = d.properties.CFSAUID;
            const fsaData = statData[fsa];
            if (fsaData) return getColour('yellow', 'red', fsaData, max, min);
            return 'gray';
        })
    g.style('visibility', 'visible') // make visible once recoloured
}


const colorMap = (max: number, min: number) => {

}

const computeMonthlyStats = (mapData: DataByMonth[]): Stats => {
    const stats: Stats = {
        'meanMonthlyUsers': 0,
        'meanMonthlyOccupiedBeds': 0,
        'meanMonthlyUnoccupiedBeds': 0,
        'meanMonthlyOccupiedRooms': 0,
        'meanMonthlyUnoccupiedRooms': 0,
        'meanMonthlyPrograms': 0,
        'meanMonthlyShelters': 0,
        'meanMonthlyOrgs': 0,
        'meanMonthlyLocations': 0,
        'maxMonthlyUsersFsa': '',
        'maxMonthlyUsersMonth': '',
        'maxMonthlyUsers': 0,
        'minMonthlyUsers': 1000000
    }
    mapData.forEach(v => {
        if (v) {
            v.data.forEach(dv => {
                stats.meanMonthlyUsers += dv.SERVICE_USER_COUNT_MEAN
                stats.meanMonthlyOccupiedBeds += dv.OCCUPIED_BEDS_MEAN
                stats.meanMonthlyUnoccupiedBeds += dv.UNOCCUPIED_BEDS_MEAN
                stats.meanMonthlyOccupiedRooms += dv.OCCUPIED_ROOMS_MEAN
                stats.meanMonthlyUnoccupiedRooms += dv.UNOCCUPIED_ROOMS_MEAN
                stats.meanMonthlyPrograms += dv.PROGRAM_COUNT
                stats.meanMonthlyShelters += dv.SHELTER_COUNT
                stats.meanMonthlyOrgs += dv.ORG_COUNT
                stats.meanMonthlyLocations += dv.LOCATION_COUNT

                if (stats.maxMonthlyUsers < dv.SERVICE_USER_COUNT_MEAN) {
                    stats.maxMonthlyUsers = dv.SERVICE_USER_COUNT_MEAN
                    stats.maxMonthlyUsersFsa = dv.LOCATION_FSA_CODE
                    stats.maxMonthlyUsersMonth = v.month
                }
                if (stats.minMonthlyUsers > dv.SERVICE_USER_COUNT_MEAN) stats.minMonthlyUsers = dv.SERVICE_USER_COUNT_MEAN
            })
        }
    })
    stats.meanMonthlyUsers = Math.round(stats.meanMonthlyUsers / mapData.length)
    stats.meanMonthlyOccupiedBeds = Math.round(stats.meanMonthlyOccupiedBeds / mapData.length)
    stats.meanMonthlyUnoccupiedBeds = Math.round(stats.meanMonthlyUnoccupiedBeds / mapData.length)
    stats.meanMonthlyOccupiedRooms = Math.round(stats.meanMonthlyOccupiedRooms / mapData.length)
    stats.meanMonthlyUnoccupiedRooms = Math.round(stats.meanMonthlyUnoccupiedRooms / mapData.length)
    stats.meanMonthlyPrograms = Math.round(stats.meanMonthlyPrograms / mapData.length)
    stats.meanMonthlyShelters = Math.round(stats.meanMonthlyShelters / mapData.length)
    stats.meanMonthlyOrgs = Math.round(stats.meanMonthlyOrgs / mapData.length)
    stats.meanMonthlyLocations = Math.round(stats.meanMonthlyLocations / mapData.length)

    return stats
}

const computeFsaStats = (mapData: DataByMonth[], fsa: string): Stats => {

    const stats: Stats = {
        'meanMonthlyUsers': 0,
        'meanMonthlyOccupiedBeds': 0,
        'meanMonthlyUnoccupiedBeds': 0,
        'meanMonthlyOccupiedRooms': 0,
        'meanMonthlyUnoccupiedRooms': 0,
        'meanMonthlyPrograms': 0,
        'meanMonthlyShelters': 0,
        'meanMonthlyOrgs': 0,
        'meanMonthlyLocations': 0,
        'maxMonthlyUsersFsa': '',
        'maxMonthlyUsersMonth': '',
        'maxMonthlyUsers': 0,
        'minMonthlyUsers': 100000
    }
    mapData.forEach(v => {
        v.data.forEach(dv => {
            if (dv.LOCATION_FSA_CODE === fsa) {
                stats.meanMonthlyUsers += dv.SERVICE_USER_COUNT_MEAN
                stats.meanMonthlyOccupiedBeds += dv.OCCUPIED_BEDS_MEAN
                stats.meanMonthlyUnoccupiedBeds += dv.UNOCCUPIED_BEDS_MEAN
                stats.meanMonthlyOccupiedRooms += dv.OCCUPIED_ROOMS_MEAN
                stats.meanMonthlyUnoccupiedRooms += dv.UNOCCUPIED_ROOMS_MEAN
                stats.meanMonthlyPrograms += dv.PROGRAM_COUNT
                stats.meanMonthlyShelters += dv.SHELTER_COUNT
                stats.meanMonthlyOrgs += dv.ORG_COUNT
                stats.meanMonthlyLocations += dv.LOCATION_COUNT

                if (stats.maxMonthlyUsers < dv.SERVICE_USER_COUNT_MEAN) {
                    stats.maxMonthlyUsers = dv.SERVICE_USER_COUNT_MEAN
                    stats.maxMonthlyUsersFsa = dv.LOCATION_FSA_CODE
                    stats.maxMonthlyUsersMonth = v.month
                }
                if (stats.minMonthlyUsers > dv.SERVICE_USER_COUNT_MEAN) stats.minMonthlyUsers = dv.SERVICE_USER_COUNT_MEAN
            }
        })
    })
    stats.meanMonthlyUsers = Math.round(stats.meanMonthlyUsers / mapData.length)
    stats.meanMonthlyOccupiedBeds = Math.round(stats.meanMonthlyOccupiedBeds / mapData.length)
    stats.meanMonthlyUnoccupiedBeds = Math.round(stats.meanMonthlyUnoccupiedBeds / mapData.length)
    stats.meanMonthlyOccupiedRooms = Math.round(stats.meanMonthlyOccupiedRooms / mapData.length)
    stats.meanMonthlyUnoccupiedRooms = Math.round(stats.meanMonthlyUnoccupiedRooms / mapData.length)
    stats.meanMonthlyPrograms = Math.round(stats.meanMonthlyPrograms / mapData.length)
    stats.meanMonthlyShelters = Math.round(stats.meanMonthlyShelters / mapData.length)
    stats.meanMonthlyOrgs = Math.round(stats.meanMonthlyOrgs / mapData.length)
    stats.meanMonthlyLocations = Math.round(stats.meanMonthlyLocations / mapData.length)

    return stats;
}

type PropsSettings = {
    selectedArea: string | null;
    mapData: DataByMonth[];
}

export function MapSettings({selectedArea, mapData}: PropsSettings) {
    const [selectedAreaData, setSelectedAreaData] = useState<any>(null);
    const [selectedHeatmapOption, setSelectedHeatmapOption] = useState<string>('SERVICE_USER_COUNT')
    const [heatmapData, setHeatmapData] = useState<StatByFsa | null>(null)
    const [monthlyStats, setMonthlyStats] = useState<Stats | null>(null);
    const [fsaStats, setFsaStats] = useState<Stats | null>(null);

    const onChange = (e: any) => {
        // a new drop-down option selected
        setSelectedHeatmapOption(e.target.value)
    }

    useEffect(() => {
        setMonthlyStats(computeMonthlyStats(mapData))
    }, [mapData])

    useEffect(() => {
        // null on first call
        setSelectedAreaData(null)

        if (!selectedArea) return;
        setFsaStats(computeFsaStats(mapData, selectedArea))
        
        const url = `http://localhost:8080/data/fsa/${selectedArea}`

        const getData: any = async () => {
            await fetch(url)
                .then((res) => res.json())
                .then((servData) => {
                    if (servData.message == 'Successful FSA data request') {
                        setSelectedAreaData(servData.data)
                    }
                    else setSelectedAreaData({}) // TODO: This should handle bad requests
                })
        }
        getData()
    }, [selectedArea])

    useEffect(() => {
        const getData = async () => {
            await fetch(`http://localhost:8080/data/by_fsa/${selectedHeatmapOption}`)
                .then((res) => res.json())
                .then((data) => {
                    setHeatmapData(data.data)
                })
        }
        getData()

    }, [selectedHeatmapOption])   
    
    useEffect(() => {
        if (heatmapData) {
            setPathColour(heatmapData)
        }
    })
    return (
        <>
            <h1 className="text-3xl">Info and options</h1>
            <h1 className="text-2xl">Heatmap statistic</h1>
            <select 
                id="selected-info"
                name="selectedInfo" 
                className="p-1 border-black border-2 mt-2 mb-1"
                onChange={onChange}
            >
                <option value="SERVICE_USER_COUNT">Service users</option>
                <option value="OCCUPIED_BEDS">Occupied beds</option>
                <option value="UNOCCUPIED_BEDS">Unoccupied beds</option>
                <option value="OCCUPIED_ROOMS">Occupied rooms</option>
                <option value="UNOCCUPIED_ROOMS">Unoccupied rooms</option>
                <option value="ORGANIZATION_ID">Active organizations</option>
                <option value="PROGRAM_ID">Active programs</option>
                <option value="SHELTER_GROUP">Active shelters</option>
            </select>
            {monthlyStats && (
                <>
                    <h1 className="text-2xl">Map statistics</h1>
                    <ul className='list-disc mx-10 text-left'>
                        <li>There are {monthlyStats.meanMonthlyUsers} average monthly service users across the city</li>
                        <li>Every month there are {monthlyStats.meanMonthlyShelters} active shelters, {monthlyStats.meanMonthlyOrgs} active organizations,<br/> and {monthlyStats.meanMonthlyPrograms} active programs on average</li>
                        <li>Programs providing beds have {monthlyStats.meanMonthlyOccupiedBeds} occupied, {monthlyStats.meanMonthlyUnoccupiedBeds} unoccupied on average</li>
                        <li>Programs providing rooms have {monthlyStats.meanMonthlyOccupiedRooms} occupied, {monthlyStats.meanMonthlyUnoccupiedRooms} unoccupied on average</li>
                        <li>The most monthly service users for an FSA were {monthlyStats.maxMonthlyUsers} within {monthlyStats.maxMonthlyUsersFsa} in {monthlyStats.maxMonthlyUsersMonth}</li>
                    </ul>
                </>
                
            )}
            <h1 className="text-xl">{selectedArea ? `FSA selected: ${selectedArea}` : 'No FSA selected'}</h1>
            <div className="">
                {selectedArea ? ((selectedAreaData && fsaStats) ? (Object.keys(selectedAreaData).length !== 0) ? (
                    <>
                        <ul className='list-disc mx-10 text-left'>
                            {fsaStats.meanMonthlyUsers !== 0 && <li>{fsaStats.meanMonthlyUsers} average service users per month</li>}
                            {fsaStats.meanMonthlyOccupiedBeds !== 0 &&<li>{fsaStats.meanMonthlyOccupiedBeds} average occupied beds per month</li>}
                            {fsaStats.meanMonthlyUnoccupiedBeds !== 0 &&<li>{fsaStats.meanMonthlyUnoccupiedBeds} average unoccupied beds per month</li>}
                            {fsaStats.meanMonthlyOccupiedRooms !== 0 &&<li>{fsaStats.meanMonthlyOccupiedRooms} average occupied rooms per month</li>}
                            {fsaStats.meanMonthlyUnoccupiedRooms !== 0 &&<li>{fsaStats.meanMonthlyUnoccupiedRooms} average unoccupied rooms per month</li>}
                            {fsaStats.meanMonthlyPrograms !== 0 &&<li>{fsaStats.meanMonthlyPrograms} active programs</li>}
                            {fsaStats.meanMonthlyOrgs !== 0 &&<li>{fsaStats.meanMonthlyOrgs} active organizations</li>}
                            {fsaStats.meanMonthlyShelters !== 0 &&<li>{fsaStats.meanMonthlyShelters} active shelters</li>}
                        </ul>
                    </>
                ) : (<>No data found...</>) : (<>Loading...</>)) : <>No selected area</>} 
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