import geopandas as gp
import geojson
import pandas as pd
import ijson
import csv
import re

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


def shrink_oda_date():
    # city = Toronto
    with open('../data/ODA_ON_v1.csv', 'r') as fin, open('../data/ODA_TORONTO.csv', 'w', newline='') as fout:
        writer = csv.writer(fout)
        for row in csv.reader(fin):
            x = re.search("Toronto", row[21])
            if x:
                writer.writerow(row)

def oda_data_df():
    chunksize = 50000
    for chunk in pd.read_csv('../data/ODA_ON_V1.csv', chunksize=chunksize):
        print(chunk['city'].unique())
        print(chunk['provider'].unique())

def addresses():
    df = pd.read_csv('../data/data_2025.csv')
    print(df.columns)
    return df['LOCATION_ADDRESS'].unique()

def find_lat_lon(addrs):
    df_addresses = pd.read_csv('../data/ODA_TORONTO.csv')
    print(df_addresses.columns)
    for addy in addrs:
        if type(addy) != str: continue # ?? skip that
        addy_parts = addy.split(' ')

        addy = ' '.join(addy_parts[:-1]) # only need number and first part?
        # misses addresses: 
        #   2387 Dundas Street, which is in the spreadsheet but names Dundas St
        #   3600 Steeles Ave
        df_addy = df_addresses[df_addresses['full_addr'].str.contains(addy)]
        if not df_addy.empty:
            lat = df_addy['latitude'].iloc[0]
            lon = df_addy['longitude'].iloc[0]
            print(f'Found address {addy} at {lat}, {lon}')
        else: print(f"Did not find address {addy}")


def main():
    # convert the shape file to a geojson file
    #shapefile_path = "../GeoData/fsa_boundary_cbf/lfsa000b21a_e.shp"
    #convert_shapefile(shapefile_path)

    # filter the geojson file for Toronto
    #geojson_path = "../GeoData/canada_fsa_codes_cbf.geojson"
    #filter_geojson(geojson_path)
    #shrink_oda_date()
    #oda_data_df()
    addrs = addresses()
    find_lat_lon(addrs)
    print("Completed main")

if __name__ == "__main__":
    main()