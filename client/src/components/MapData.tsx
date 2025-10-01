import { useEffect, useState } from "react"

export function MapData({area, isFsa}: {area: string, isFsa: any}) {
    const [areaData, setAreaData] = useState<string[] | null>(null)
    const [selectedInfoList, setSelectedInfoList] = useState<string[]>([])
    const [selectedInfoOption, setSelectedInfoOption] = useState('active_orgs')

    useEffect(() => {
        if (!area) return;
        setAreaData(null)
        setSelectedInfoList([])

        const url = isFsa ? `http://localhost:8080/data/fsa/${area}` : `http://localhost:8080/data/nb/${area}`

        const getData: any = async () => {
            await fetch(url)
                .then((res) => res.json())
                .then((servData) => {
                    console.log({servData})
                    setAreaData(servData.data)
                })
                .then(() => setInfoList())
        }
        getData()
    }, [area])
    const setInfoList = () => {
        if (!areaData) return;

        const e = document.getElementById('selectedInfo') as HTMLSelectElement
        if (e) { // TODO: Why does this not show on first run?

            const selectedKey = e.value as string
            setSelectedInfoOption(selectedKey)
            const val = areaData[selectedKey] as string[] // TODO: Fix accessing by key
            console.log({areaData}, {val})
            setSelectedInfoList(val)
        } else {
            // then we know if is first render
            const val = areaData[selectedInfoOption] as string[]
            setSelectedInfoList(val)
        }
    }
    const onChange = () => {
        setInfoList()
    }
    return (
        <div>
            <h2 className="text-[24px] font-bold">Area information</h2>
            {area.length > 1 && (
                <>
                    <h2 className='text-[16px] mb-4'>{isFsa ? "FSA" : "Neighbourhood"} selected: {area}</h2>
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
                            
                            {selectedInfoList.length > 0 ? (
                                <ul className='list-disc ml-5'>
                                {selectedInfoList.map((v, i) => {
                                    return (
                                        <li key={i}>{v}</li>
                                    )
                                })}
                                </ul>
                                ) : (<><p>No data found</p></>)
                            }
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
