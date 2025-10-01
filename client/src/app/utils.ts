import { ServerData } from "@/types/Data";

// used to make initial API calls for components
export async function fetchDataBeforeLoad(url: string): Promise<ServerData> {
  try {
    const res = await fetch(url);
    const data = await res.json();

    return data;
  } catch (e) {
    console.log("Error when fetching from server")
    console.log({e})
    const empty: ServerData = { message: "Error when fetching from server", data: {}}
    return empty
  }
  
}
