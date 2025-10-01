import { useEffect } from "react"

// used to choose the geojson base and select the heatmap filter
export function MapOptions({ mapFilter, setMapFilter, isFsa, setIsFsa }: { mapFilter: any, setMapFilter: any, isFsa: any, setIsFsa: any }) {
    const handleToggleFsa = () => {
        setIsFsa(true)
    }
    const handleToggleNb = () => {
        setIsFsa(false)
    }

    useEffect(() => {
        setMapFilter('entryFrequency')

        const radio1 = document.getElementById('fsa-toggle') as HTMLInputElement
        const radio2 = document.getElementById('nb-toggle') as HTMLInputElement

        if (radio1 && radio2) {
            radio1.checked = isFsa;
            radio2.checked = !isFsa;
        }
    }, [])

    const onSelectChange = () => {
        const e = document.getElementById('selectedMapFilter') as HTMLSelectElement
        if (e) { // TODO: does not run on first run
            const selectedKey = e.value as string
            setMapFilter(selectedKey)
        }
    }
    return (
        <div className='grid content-normal'>
            <h2 className="text-[30px]">Options</h2>
            <label>
                <input id='fsa-toggle' type='radio' name='map-base' onClick={handleToggleFsa}/> By FSA<br/>
                <input id='nb-toggle' type='radio' name='map-base' onClick={handleToggleNb}/> By neighbourhood<br/>
            </label>
            <label>
                Filter:{' '}
                <select 
                    id='selectedMapFilter'
                    name="mapFilter" 
                    className="p-0.5 border-2 border-solid text-center"
                    onChange={onSelectChange}
                >
                    <option value="entryFrequency">Entry frequency</option>
                    <option value="meanProgramUsers">Average daily program users</option>
                    <option value="meanOpenBeds">Average daily open beds</option>
                </select>
                <br/>
            </label>
        </div>
    )
}