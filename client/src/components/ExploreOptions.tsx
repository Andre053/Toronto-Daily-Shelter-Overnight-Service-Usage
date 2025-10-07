import { useEffect, useState } from "react";
import { ServiceUserDataAll } from "@/types/Data";
import * as d3 from "d3";

export const getFilterData = async (urlEndpoint: string, setFilterData: any): Promise<any> => {
    const url = `http://localhost:8080/data/complete/${urlEndpoint}`

    fetch(url)
        .then((res) => res.json())
        .then((data: ServiceUserDataAll) => {
            console.log('[MapOptions] Set filter data to', {data})
            setFilterData(data.data)
        })
    return {}
}

const getColour = (colourStart: string, colourEnd: string, value: number, max: number) => {
    const colourScale = d3.scaleLinear([0, max], [colourStart, colourEnd])

    return colourScale(value)
}

const setPathColour = (statName: string, maxVal: number, filterData: any) => {
    const g = d3.select('#map-group'); // should only be a single g tag

    g.selectAll('path') // go through all paths and change the colour
        .classed('stroke-black', true)
        .attr('fill', (d: any) => {
            const fsa: string = d.properties.CFSAUID;
            const fsaData = filterData[fsa];
            if (fsaData) return getColour('yellow', 'red', fsaData[statName], maxVal);
            //console.log('Could not find', fsa, {filterData})
            return 'gray';
        })
    g.style('visibility', 'visible') // make visible once recoloured
}

// TODO: Decide future of this componenet
function radioOptions({isFsa, setIsFsa}: {isFsa: boolean, setIsFsa: any}) {
    const handleToggleFsa = () => {
        setIsFsa(true);
    };
    const handleToggleNb = () => {
        setIsFsa(false);
    };

    useEffect(() => {
        const radio1 = document.getElementById('fsa-toggle') as HTMLInputElement;
        const radio2 = document.getElementById('nb-toggle') as HTMLInputElement;

        if (radio1 && radio2) {
            radio1.checked = isFsa;
            radio2.checked = !isFsa;
        };
    }, []);

    return (
        <label>
            <input id='fsa-toggle' type='radio' name='map-base' onClick={handleToggleFsa}/> By FSA<br/>
            <input id='nb-toggle' type='radio' name='map-base' onClick={handleToggleNb}/> By neighbourhood<br/>
        </label>
    )
}

// TODO: Fix auto-setting the map filter
// used to choose the geojson base and select the heatmap filter

type Props = {
    filterData: ServiceUserDataAll | null;
}

export function MapOptions({ filterData}: Props) {
    const [filterKey, setFilterKey] = useState<string | null>(null); // TODO: This should automatically colour the map

    useEffect(() => {
        console.log('[MapOptions] filterKey useEffect called')
        if (filterData && filterKey) {
            console.log('Colouring map')
            const getMax = (stat: string) => {
                let max = 0;
                for (const key in filterData) {
                    const cur = filterData[key][stat]
                    if (cur > max) max = cur
                }
                return max
            }
            if (filterKey == 'dailyServiceUsers') {
                const maxSum = getMax('total_sum')
                setPathColour('total_sum', maxSum, filterData)
            } 
        }
        if (!filterKey) { // set filter key
            setFilterKey('dailyServiceUsers');
            
        }
    }, [filterKey, filterData])

    const onSelectChange = () => {
        const e = document.getElementById('selectedMapFilter') as HTMLSelectElement
        if (e) { // TODO: does not run on first run
            const selectedKey = e.value as string
            setFilterKey(selectedKey)
        }
    }
    return (
        <div className='grid'>
            <h2 className="text-[24px]"><b>Data options</b></h2>
            <div className="grid ml-2">
                <label className="text-[16px]">Selected feature</label>
                <select 
                    id='selectedMapFilter'
                    name='mapFilter' 
                    className="p-1 my-2 border-2 border-solid text-center"
                    onChange={onSelectChange}
                >
                    <option value="dailyServiceUsers">Daily service users</option>
                </select>
            </div> 
            
        </div>
    )
}