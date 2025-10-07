import { ChartOpts, ChartOption } from "@/types/Data";
import { useEffect } from "react";

type Props = {
    selectedOptions: ChartOpts | null;
    setSelectedOptions: any;
}
export function ChartOptions({ selectedOptions, setSelectedOptions}: Props) {

    // what options are available to choose from?
    useEffect(() => {
        console.log(selectedOptions)
    }, [])

    const onChange = (e: any) => {
        if (!selectedOptions) return; 

        const checkStatus = e.target.checked
        const optionSelected = e.target.attributes[0].value
        const statName = e.target.attributes[3].value

        const selectedOptionsChange = selectedOptions;
        selectedOptionsChange[statName][optionSelected].selectedStatus = checkStatus;
        
        setSelectedOptions(selectedOptionsChange)
    }

    return (
        <div>
            <h1 className="text-[24px]">CHART OPTIONS</h1>
            {selectedOptions && (
                <>
                    {Object.keys(selectedOptions).map((stat) => (
                        <>
                            <h1 className="text-[18px]">{stat.replace('_', ' ')}</h1><br/>
                            <ul>
                                {selectedOptions[stat].map((v, i) => (
                                    <>
                                        <li key={i}>
                                            <input type='checkbox' id={v.dataKey} name={stat} value={v.dataKey} defaultChecked={v.selectedStatus} onChange={onChange}/>
                                            <label id={v.dataKey + '-label'}> {v.displayName}</label>
                                        </li>
                                    </>
                                )
                            )}
                            </ul>
                        </>
                    ))}
                </>
            )}
        </div>
    )
}