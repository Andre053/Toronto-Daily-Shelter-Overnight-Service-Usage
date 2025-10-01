import geopandas as gp
import geojson
import pandas as pd
import ijson

# UTILITIES.py
# - Used to prep the geojson data

JSON_BASE = {
    "type": "FeatureCollection",
    "name": "toronto_fsa_codes_generated",
    "crs": { 
        "type": "name", 
        "properties": { 
                "name": "urn:ogc:def:crs:EPSG::3347" 
            } 
        },
    "features": []
}
# ['M7A', 'M5X'] not found
FSV_CODES = "'M4V' 'M4S' 'M4C' 'M8Y' 'M8W' 'M1H' 'M6S' 'M6E' 'M2M' 'M3C' 'M4T' 'M1L' 'M6G' 'M6H' 'M6A' 'M6B' 'M5R' 'M4K' 'M5T' 'M4G' 'M1S' 'M3A' 'M1N' 'M9C' 'M6J' 'M6K' 'M4L' 'M5S' 'M6M' 'M4E' 'M8V' 'M5A' 'M6N' 'M5N' 'M9A' 'M6R' 'M4B' 'M4J' 'M3H' 'M9M' 'M9R' 'M4N' 'M2K' 'M9N' 'M3L' 'M4A' 'M1B' 'M9W' 'M6C' 'M8Z' 'M5P' 'M5M' 'M4R' 'M2J' 'M2N' 'M4W' 'M1C' 'M4M' 'M6P' 'M1M' 'M1K' 'M3B' 'M9L' 'M1E' 'M2R' 'M1R' 'M2H' 'M4X' 'M9B' 'M1X' 'M5V' 'M4P' 'M6L' 'M2P' 'M2L' 'M8X' 'M5H' 'M1P' 'M9V' 'M5B' 'M1J' 'M9P' 'M3M' 'M3K' 'M1T' 'M1V' 'M3N' 'M3J' 'M1G' 'M1W' 'M4H' 'M4Y' 'M5C' 'M5J' 'M5E' 'M5G' 'M7A' 'M5X'".replace("'", "").split(" ")

# convert to the correct GeoJSON, needs to be compliant with Leaflet system
# this requires re-projecting (https://geopandas.org/en/stable/docs/user_guide/projections.html)
def convert_shapefile(path):
    shape_file = gp.read_file(path)
    print("CRS data:", shape_file.crs)
    input("Convert to GeoJSON?")

    shape_file = shape_file.to_crs("EPSG:4326")
    print("CRS data is now:", shape_file.crs)
    input("Complete the change?")
    shape_file.to_file("../GeoData/canada_fsa_codes_cbf.geojson", driver='GeoJSON')

# only want those FSA codes within Toronto
# this needs to be changed...
def get_postal_codes(): 
    path = "daily_overnight_occupancy.csv"
    df = pd.read_csv(path)
    return df["POSTAL"].unique()

def filter_geojson(path):
    data = JSON_BASE

    with open(path, "r") as f:
        features = ijson.items(f, "features.item") # parse all features
        print("Parser ready with features")
        
        keep = [feat for feat in features if feat['properties']['CFSAUID'] in FSV_CODES]
        data["features"] = keep

    #gj_features = [Feature(geometry=x["geometry"], properties=x[]) for x in data["features"]]
    #geojson_data = None

    with open("../GeoData/GeoJsons/tor_fsa_cbf.geojson", "w") as f:
        geojson.dump(data, f, indent=2)
    print("Dumped JSON")

    missing_fsvs = [f for f in FSV_CODES if f not in [x["properties"]["CFSAUID"] for x in data["features"]]]
    print("Missing FSVs:", missing_fsvs)

def main():
    # convert the shape file to a geojson file
    shapefile_path = "../GeoData/fsa_boundary_cbf/lfsa000b21a_e.shp"
    convert_shapefile(shapefile_path)

    # filter the geojson file for Toronto
    geojson_path = "../GeoData/canada_fsa_codes_cbf.geojson"
    filter_geojson(geojson_path)
    print("Completed main")

if __name__ == "__main__":
    main()