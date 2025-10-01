// not currently used
// was used to gather initial heatmap data
export async function GET() {
    const res = await fetch('http://localhost:8080/mapdata');
    const json = await res.json();

    return new Response(JSON.stringify(json), {
        headers: {'Content-Type': 'application/json'}
    })
};