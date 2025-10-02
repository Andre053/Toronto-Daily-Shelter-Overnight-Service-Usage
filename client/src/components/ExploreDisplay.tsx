import { useContext } from "react"
import { TabContext } from "./Explore"
import { MapOptions } from "./ExploreOptions"
import { MapData } from "./MapData"
import { ServiceUserDataAll } from "@/types/Data"
import { filter } from "d3"

type Props = {
    filterData: ServiceUserDataAll | null;
    selectedArea: string;
}
export function ExploreDisplay({filterData, selectedArea}: Props) {
    const {selectedTab} = useContext(TabContext);

    return (
        <>
            {selectedTab == 'tab-overview' && (
                <div className="w-full h-full text-center content-center text-[24px]">
                        Select a tab to see more...
                </div>
            )}
            {(selectedTab == 'tab-map') && (
                <>
                    <MapOptions filterData={filterData}/><br/>
                    <MapData filterData={filterData} area={selectedArea}/>
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