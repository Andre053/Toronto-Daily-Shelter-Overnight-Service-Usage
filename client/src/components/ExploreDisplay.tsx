import { useContext } from "react"
import { TabContext } from "./Explore"
import { MapOptions } from "./ExploreOptions"
import { MapData } from "./MapData"

type Props = {
    filterData: any;
    isFsa: boolean;
    setIsFsa: any;
    mapGenerated: boolean;
    selectedArea: string;
}
export function ExploreDisplay({filterData, isFsa, setIsFsa, mapGenerated, selectedArea}: Props) {
    const {selectedTab} = useContext(TabContext);
    
    return (
        <>
            {selectedTab == 'tab-overview' && (
                <>
                    Select a tab to see more...
                </>
            )}
            {selectedTab == 'tab-map' && (
                <>
                    <MapOptions filterData={filterData} isFsa={isFsa} setIsFsa={setIsFsa} mapGenerated={mapGenerated}/><br/>
                    <MapData filterData={filterData} area={selectedArea} isFsa={isFsa}/>
                </>
            )}
            {selectedTab == 'tab-line' && (
                <>
                    Line data, eventually...
                </>
            )}

        </>
    )
}