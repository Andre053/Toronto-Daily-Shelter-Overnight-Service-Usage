"""
python -m venv <path>
- Intall fastapi, jsonify
- pip install "uvicorn[standard]"
fastapi dev main.py

Dates are YYYY-MM-DD

TODO
- Implement query parameters with dates
- Fix daily updating using globals file
- Divide code into multiple files
- Implement APIRouter groupings

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn
import requests as req
from urllib.request import urlretrieve
import csv, os
from datetime import datetime
import pandas as pd
import geojson, ijson
import numpy as np

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

FSV_CODES = "'M4V' 'M4S' 'M4C' 'M8Y' 'M8W' 'M1H' 'M6S' 'M6E' 'M2M' 'M3C' 'M4T' 'M1L' 'M6G' 'M6H' 'M6A' 'M6B' 'M5R' 'M4K' 'M5T' 'M4G' 'M1S' 'M3A' 'M1N' 'M9C' 'M6J' 'M6K' 'M4L' 'M5S' 'M6M' 'M4E' 'M8V' 'M5A' 'M6N' 'M5N' 'M9A' 'M6R' 'M4B' 'M4J' 'M3H' 'M9M' 'M9R' 'M4N' 'M2K' 'M9N' 'M3L' 'M4A' 'M1B' 'M9W' 'M6C' 'M8Z' 'M5P' 'M5M' 'M4R' 'M2J' 'M2N' 'M4W' 'M1C' 'M4M' 'M6P' 'M1M' 'M1K' 'M3B' 'M9L' 'M1E' 'M2R' 'M1R' 'M2H' 'M4X' 'M9B' 'M1X' 'M5V' 'M4P' 'M6L' 'M2P' 'M2L' 'M8X' 'M5H' 'M1P' 'M9V' 'M5B' 'M1J' 'M9P' 'M3M' 'M3K' 'M1T' 'M1V' 'M3N' 'M3J' 'M1G' 'M1W' 'M4H' 'M4Y' 'M5C' 'M5J' 'M5E' 'M5G' 'M7A' 'M5X'".replace("'", "").split(" ")

DATA_PATH = "../data/data_2025.csv"
GEOJSON_FSA_PATH = "../data/GeoJson/tor_fsa_cbf.geojson"
GEOJSON_NB_PATH = "../data/GeoJson/tor_neighbourhoods.geojson"

DATA_LAST_UPDATED = "Monday, 29. September 2025"
app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# TODO: Implement running everyday
def download_all_data_csv():
    current_date = datetime.now().strftime("%A, %d. %B %Y")
    
    # check if already imported today
    if DATA_LAST_UPDATED == str(current_date):
        print('Data is already up to date')
        return
    
    print(f"Data last updated on {DATA_LAST_UPDATED}, updating now on {str(current_date)}")
    
    set_DATA_LAST_UPDATED(str(current_date))

    BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    PACKAGE = "daily-shelter-overnight-service-occupancy-capacity"

    url = BASE_URL + "/api/3/action/package_show"
    params = {"id": PACKAGE}

    dir = os.getcwd()

    package = req.get(url, params=params).json()
    print("Retrieved package\n\n\n")

    for i, resource in enumerate(package['result']['resources']):
        if resource['datastore_active']:
            # get all records in CSV
            url = BASE_URL + '/datastore/dump/' + resource['id']

            filename = os.path.join(dir, f"../data/data_{resource['id']}.csv")
            urlretrieve(url=url, filename=filename)
        if not resource['datastore_active']:
            url = BASE_URL + '/api/3/action/resource_show?id=' + resource['id']
            resource_metadata = req.get(url).json()

# parameters are documented: https://docs.ckan.org/en/latest/maintaining/datastore.html
# TODO: Implement with a API endpoint
def download_specific_data():
    BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    PACKAGE = "daily-shelter-overnight-service-occupancy-capacity"

    url = BASE_URL + "/api/3/action/package_show"
    params = {"id": PACKAGE}

    package = req.get(url, params=params).json()

    for i, resource in enumerate(package['result']['resources']):
        if resource['datastore_active']:
            url = BASE_URL + '/api/3/action/datastore_search'
            p = {'id': resource['id']}
            resource_search_data = req.get(url, params = p).json()['result']
            print(resource_search_data)

def get_geojson_data(geotype):
    if geotype == "fsa": path = GEOJSON_FSA_PATH
    elif geotype == "neighbourhood": path = GEOJSON_NB_PATH
    else: return {}

    with open(path, 'r') as f:
        return json.load(f)

def prep_data(df):
    df['LOCATION_FSA_CODE'] = df['LOCATION_POSTAL_CODE'].apply(lambda x: x[:3] if pd.notnull(x) else "N/A")
    return df

def load_dataframe():
    return pd.read_csv(DATA_PATH)

# TODO: Add more data to send
# Used when a FSA is selected on the map
def get_area_data(area, area_type):
    df = get_data(None)

    if area_type == 'fsa':
        df = df[df['LOCATION_FSA_CODE'] == area]
    if area_type == 'nb':
        df = df[df['PROGRAM_AREA'] == area]

    return analyze_area_data(df, area)

# filter dataframe based on list of columns
def get_data(col_filter):
    df = load_dataframe()

    df = df[['OCCUPANCY_DATE', 'ORGANIZATION_NAME', 'ORGANIZATION_ID', 'SHELTER_ID', 'SHELTER_GROUP', 'LOCATION_NAME', 'LOCATION_ID', 'LOCATION_ADDRESS', 'LOCATION_POSTAL_CODE', 'PROGRAM_ID', 'PROGRAM_NAME', 'PROGRAM_MODEL', 'SECTOR', 'OVERNIGHT_SERVICE_TYPE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'UNAVAILABLE_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS']]
    df = prep_data(df)

    if col_filter: return df[col_filter]
    return df

def get_map_filter_cols(filter):
    if filter == 'serviceUsers': # average daily service user count TODO: Rename
        return ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT']
    elif filter == 'option2': # average daily occupied beds TODO: Rename
        return ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'OCCUPIED_BEDS']
    elif filter == 'option3': # average daily occupied rooms TODO: Rename
        return ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'OCCUPIED_ROOMS']
    elif filter == 'programCount': # unique program counts active in the timeline 
        return ['LOCATION_FSA_CODE', 'PROGRAM_NAME']
    elif filter == 'shelterCount': # shelter counts
        return ['OCCUPANCY_DATE' 'LOCATION_FSA_CODE', 'SHELTER_ID']
    else: 
        return []

# TODO: No longer will be used, think of new approach for heat map data
def analyze_fsa(df):
    val_counts = df['LOCATION_FSA_CODE'].value_counts()
    max_count = int(val_counts.max())

    vc_json = [{'key': str(idx), 'val': int(count)} for idx, count in val_counts.items()]

    payload = {
        "fsa": vc_json,
        "stats": {
            "max": max_count,
        }
    }
    return payload

def analyze_area_data(df, area):
    # there may be multiple names of the same datapoint, for counts, use ID
    # TODO: Only use the most recent name if multiple, currently we send all names
    active_programs = df['PROGRAM_NAME'].unique().tolist() 
    active_programs_count = len(df['PROGRAM_ID'].unique())
    service_types = df['OVERNIGHT_SERVICE_TYPE'].unique().tolist()
    active_organizations = df['ORGANIZATION_NAME'].unique().tolist()
    active_organizations_count = len(df['ORGANIZATION_ID'].unique()) 
    shelters = df['LOCATION_NAME'].unique().tolist()
    shelters_count = len(df['LOCATION_ID'].unique())

    analytic_cols = ['OCCUPANCY_DATE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'UNAVAILABLE_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS']
    df_by_date = df[analytic_cols].groupby(['OCCUPANCY_DATE'])
    means = df_by_date.mean().replace({np.nan: None})
    mean_dict = means.head(50).to_dict()


    payload = {
        "area": area,
        "active_programs": active_programs,
        "active_programs_count": active_programs_count,
        "service_types": service_types,
        "shelters": shelters,
        "shelters_count": shelters_count,
        "active_orgs": active_organizations,
        "active_orgs_count": active_organizations_count,
        "means": mean_dict
    }
    return payload

def analyze_daily_service_user_count(df):
    # for each fsa_code, get all dates, sum the user_count values on each date
    data = {}

    # group-by changed it form the regular DF
    # TODO: Is there a faster solution? 
    for fsa in df['LOCATION_FSA_CODE'].unique(): 
        df_by_fsa = df[df['LOCATION_FSA_CODE'] == fsa] # breaking here
        data[fsa] = {
            'total_sum': 0,
            'total_mean': 0,
            'daily_stats': []
        }
        total_sum = 0
        total_mean = 0
        for date in df_by_fsa['OCCUPANCY_DATE'].unique():
            df_for_data = df_by_fsa[df_by_fsa['OCCUPANCY_DATE'] == date]
            daily_user_count_sum = int(df_for_data['SERVICE_USER_COUNT'].sum()) # int64 not serializable, cast to int()
            daily_user_count_mean = round(df_for_data['SERVICE_USER_COUNT'].mean(), 2)
            total_sum += daily_user_count_sum
            if daily_user_count_sum > 0: total_mean += 1 # keep track of days with counts

            data[fsa]['daily_stats'].append({'DATE': date, 'SERVICE_USER_SUM': daily_user_count_sum, 'SERVICE_USER_MEAN': daily_user_count_mean})
        data[fsa]['total_sum'] = total_sum 
        data[fsa]['total_mean'] = round(total_sum/total_mean, 2)
    print(f'[analyze_daily_service_user_count] data creation completed with length {len(data)}')

    return data

def analyze_filter_type(df, filter):
    if filter == 'serviceUsers': # average daily service user count TODO: Rename
        return analyze_daily_service_user_count(df)
    elif filter == 'option2': # average daily occupied beds TODO: Rename
        return analyze_daily_service_user_count(df)
    elif filter == 'option3': # average daily occupied rooms TODO: Rename
        return analyze_daily_service_user_count(df)
    elif filter == 'programCount': # unique program counts active in the timeline 
        return analyze_daily_service_user_count(df)
    elif filter == 'shelterCount': # shelter counts
        return analyze_daily_service_user_count(df)
    else: 
        return []

@app.get("/")
async def root():
    download_all_data_csv()
    payload = {
        'message': 'Root has no data to give',
        'data': {}
    }
    return payload

@app.get("/geodata/{geotype}")
async def get_geo_data(geotype: str, end: str = '2025-09-01', start: str = '2025-01-01'):
    print(f'[get_geo_data] Received geotype {geotype}, end time {end}, start time {start}')
    geojson = get_geojson_data(geotype)
    payload = {
        'message': 'GeoJson data retrieved',
        'data': geojson
    }
    return payload

#TODO: Add URL parameters to customize the request being made to the backend
@app.get("/data/complete/{filter_type}") 
async def get_map_data(filter_type: str, end: str = '2025-09-01', start: str = '2025-01-01'):
    print(f'[get_map_data] Received filter {filter_type}, end time {end}, start time {start}')

    cols = get_map_filter_cols(filter_type)
    if len(cols) == 0: return {'message': f'Invalid filter type "{filter_type}" provided', 'data': {}}

    filtered_data = get_data(cols)
    
    data_json = analyze_filter_type(filtered_data, filter_type)

    payload = {
        'message': f'Data retrieved for map filter {filter_type}',
        'data': data_json,
    }
    return payload

@app.get("/data/fsa/{fsa_code}")
async def data_by_fsa(fsa_code: str, end: str = '2025-09-01', start: str = '2025-01-01'):
    data = get_area_data(fsa_code, 'fsa')

    payload = {
        'message': f'{fsa_code} data requested.',
        'data': data,
    }
    return payload

@app.get("/data/nb/{neighbourhood}")
async def data_by_fsa(neighbourhood: str):
    print("Received neighbourhood:", neighbourhood)

    return {'message': 'No data available for neighbourhoods', 'data': {}}

# TODO: Finish implementing
def set_globals():
    global DATA_LAST_UPDATED

    DATA_LAST_UPDATED = str(data['DATA_LAST_UPDATED'])

    with open("globals.json", "r") as f:
        data = json.load(f)
        set_globals(data)

# TODO: Finish implementing
def set_DATA_LAST_UPDATED(current_date_str):
    global DATA_LAST_UPDATED
    DATA_LAST_UPDATED = current_date_str
    
    with open("globals.json", "w") as f:
        data = {
            'DATA_LAST_UPDATED': current_date_str
        }
        json.dump(data, f)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True) # run the server manually

    