'''
GLOBALS
- GEOJSON_FSA_PATH
- GEOJSON_NB_PATH

FUNCTIONS
- get_geojson_data
'''
import json
import api_resources as ar
import pandas as pd

def get_geojson_data(geotype):
    if geotype == "fsa": path = ar.GEOJSON_FSA_PATH
    elif geotype == "neighbourhood": path = ar.GEOJSON_NB_PATH
    else: return {}

    with open(path, 'r') as f:
        return json.load(f)


def get_shelter_locations(df):
    addresses = df['LOCATION_ADDRESS', 'SHELTER_ID', 'SHELTER_NAME'].unique()
    print(f"Addresses {addresses}")

    grouped = df.groupby(['LOCATION_ADDRESS', 'SHELTER_ID', 'SHELTER_NAME'])

    location = find_lat_lon(addresses)

    return {}

def find_lat_lon(addresses):
    df_addresses = pd.read_csv('../data/ODA_TORONTO.csv')
    data = []
    for addy in addresses:
        if type(addy) != str: continue # ?? skip that
        addy_parts = addy.split(' ')

        addy = ' '.join(addy_parts[:-1]) # only need number and first part?
        # TODO: misses addresses: 
        #   2387 Dundas Street, which is in the spreadsheet but names Dundas St
        #   3600 Steeles Ave
        df_addy = df_addresses[df_addresses['full_addr'].str.contains(addy)] # could use better regex here
        if not df_addy.empty:
            lat = df_addy['latitude'].iloc[0]
            lon = df_addy['longitude'].iloc[0]
            print(f'Found address {addy} at {lat}, {lon}')
            data.append({
                'address': addy,
                'lat': lat,
                'lon': lon
            })
        else: print(f"Did not find address {addy}")
    return data