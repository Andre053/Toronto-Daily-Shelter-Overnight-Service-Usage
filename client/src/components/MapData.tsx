import { useEffect, useState, useContext } from "react"
import { ThemeContext } from "@emotion/react"

type dataStats = {
    totalAvgServiceUsers: string;
    fsaWithHighestAvgServiceUsers: string;
    highestAvgServiceUsers: string;
}

// TODO: Handle when FSA has no data
export function MapData({filterData, area, isFsa}: {filterData: any, area: string, isFsa: any}) {
    const [areaData, setAreaData] = useState<any>(null)
    const [selectedInfoOption, setSelectedInfoOption] = useState('active_orgs')
    const [selectedInfoList, setSelectedInfoList] = useState([])

    const [filterDataStats, setFilterDataStats] = useState<dataStats | null>(null)

    const currentTab = useContext(ThemeContext) as string // TODO: May be a better way

    useEffect(() => {
        // once filter data is set
        if (!filterData) return;

        let total = 0;
        let max = 0;
        let fsa = ''

        for (let key in filterData) {
            const totalMean = filterData[key]['total_mean']
            total += totalMean
            if (totalMean > max) {
                max = totalMean;
                fsa = key
            }
        }
        const totalString = total.toFixed(2)
        
        const maxString = max.toString()

        const stats: dataStats = {
            totalAvgServiceUsers: totalString,
            fsaWithHighestAvgServiceUsers: fsa,
            highestAvgServiceUsers: maxString
        }
        setFilterDataStats(stats)
    }, [filterData])

    useEffect(() => {
        if (!area) return;
        setAreaData(null); // clear set area data

        const url = isFsa ? `http://localhost:8080/data/fsa/${area}` : `http://localhost:8080/data/nb/${area}`

        const getData: any = async () => {
            await fetch(url)
                .then((res) => res.json())
                .then((servData) => {
                    setAreaData(servData.data)
                })
        }
        getData()
    }, [area])

    useEffect(() => {
        if (!areaData) return;
        setSelectedInfoList(areaData[selectedInfoOption])
    }, [selectedInfoOption, areaData])

    const onChange = (v: any) => {
        // a new drop-down option selected
        console.log({v})
        setSelectedInfoOption(v)
    }
    return (
        <div className="grid">
            <h2 className="text-[24px] font-bold">Stats and information</h2>
            <h2 className="text-[16px] font-bold">Total</h2>
            {filterDataStats && (
                <>
                    <ul className='list-disc ml-5'>
                        <li>There are {filterDataStats.totalAvgServiceUsers} average daily users across the city</li>
                        <li>The highest average daily service users is {filterDataStats.highestAvgServiceUsers} in {filterDataStats.fsaWithHighestAvgServiceUsers} </li>
                    </ul>
                </>
            )}
            <h2 className="text-[16px] font-bold">Area</h2>
            {area.length > 1 && (
                <>
                    <h2 className='text-[16px]'>{isFsa ? "FSA" : "Neighbourhood"} selected: {area}</h2>
                    {areaData && filterDataStats && (
                            <ul className='list-disc ml-5'>
                                <li>{Math.round(filterData[area]['total_mean'])} average service users per day</li>
                                <li>{areaData['active_orgs_count']} active organization</li>
                                <li>{areaData['shelters_count']} active shelters</li>
                                <li>{areaData['active_programs_count']} active programs</li>
                            </ul>
                    )}
                    <select 
                        id="selectedInfo"
                        name="selectedInfo" 
                        className="p-1 border-black border-2"
                        onChange={onChange}
                    >
                        <option value="active_orgs">Active organizations</option>
                        <option value="active_programs">Active programs</option>
                        <option value="service_types">Active service types</option>
                        <option value="shelters">Active shelters</option>
                    </select>
                    {!areaData && <p>Loading data...</p>}
                    {areaData && (
                        <>
                            <ul className='list-disc ml-5'>
                            {selectedInfoList.map((v, i) => {
                                return (
                                    <li key={i}>{v}</li>
                                )
                            })}
                            </ul>
                        </>
                    )}
                        
                </>
            )}
            {area.length === 0 && (
                <p>Select {isFsa ? "an FSA" : "a neighbourhood"} on the map to view stats...</p>
            )}
        </div>
    )
}
