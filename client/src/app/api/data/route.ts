// not yet used
// TODO: Route for getting specific data from backend using query parameters
export async function GET() {

    // TODO: Process path parameters

    const res = await fetch('http://localhost:8080/data'); // get FSA data by default
    const json = await res.json();

    return new Response(JSON.stringify(json), {
        headers: {'Content-Type': 'application/json'}
    })
};