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

GLOBALS_PATH = "./globals.json"
DATA_PATH = "../data/data_2025.csv"
GEOJSON_FSA_PATH = "../data/GeoJson/tor_fsa_cbf.geojson"
GEOJSON_NB_PATH = "../data/GeoJson/tor_neighbourhoods.geojson"

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
# TODO: Only run for 2025 dataset
def download_all_data_csv():
    BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    PACKAGE = "daily-shelter-overnight-service-occupancy-capacity"

    url = BASE_URL + "/api/3/action/package_show"
    params = {"id": PACKAGE}

    dir = os.getcwd()

    package = req.get(url, params=params).json()

    package_name_2025 = 'Daily shelter overnight occupancy'
    for i, resource in enumerate(package['result']['resources']):
        if resource['datastore_active']:
            # get 2025 records in CSV
            url = BASE_URL + '/api/3/action/resource_show?id=' + resource['id']
            metadata = req.get(url).json()
            if not metadata or metadata['result']['name'] != package_name_2025: continue

            url = BASE_URL + '/datastore/dump/' + resource['id']
            filename = os.path.join(dir, f"../data/data_2025.csv")
            urlretrieve(url=url, filename=filename)

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

def get_last_updated_date():
    with open(GLOBALS_PATH, 'r') as f:
        data = json.load(f)
        return data['DATA_LAST_UPDATED']


def set_last_updated_date():
    current_date = datetime.now().strftime('%Y/%m/%d')
    data = {'DATA_LAST_UPDATED': f'{current_date}'}
    with open(GLOBALS_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def load_dataframe():
    current_date = datetime.now().strftime('%Y/%m/%d')
    
    # check if already imported today
    last_updated = get_last_updated_date()
    if not (current_date == last_updated):
        print('Data is not up to date')
        download_all_data_csv()
        set_last_updated_date()
    return pd.read_csv(DATA_PATH)

# TODO: Add more data to send
# Used when a FSA is selected on the map
def get_area_data(area, area_type):
    df = get_data(None)

    if area_type == 'fsa':
        df = df[df['LOCATION_FSA_CODE'] == area]
        #print(df.head())
        if df.empty: 
            print('No records for FSA:', area)
            return None
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
    
    #print(f'[analyze_daily_service_user_count] data creation completed with length {len(data)}')
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
    

def data_by_feature(df, stat, feat_id, feat_name):
    """
    data: {
        start_date: string,
        end_date: string,
        data_by_shelter: {
            name+shelter_id: [] // with zeros for empty
        }
        want active user count, occupied beds/rooms, unoccupied beds/rooms
    }
    """
    dates = df['OCCUPANCY_DATE'].unique()
    data = {
        'statName': stat,
        'startDate': dates[0],
        'endDate': dates[-1],
        'dataByFeature': {}
    }
    print("Running data for", feat_name, stat)
    feature_ids = df[feat_id].unique()
    feature_pairs = [] # fill with shelter names
    for id in feature_ids:
        df_feat_id = df[df[feat_id] == id]
        name = '/'.join([n.replace(" ", "_") for n in df_feat_id[feat_name].unique()])
        name = name.replace("'", "").replace(",", "").replace('_-_', '_').lower() # cleaning names
        feature_pairs.append((name, id))
        data['dataByFeature'][f'{name}_{id}'] = []

    # TODO: Looping is extremely slow, use vectorization
    for date in dates:
        df_date = df[df['OCCUPANCY_DATE'] == date] # would a group by date then sum be better?
        for pair in feature_pairs:
            name = pair[0]
            id = pair[1]
            records = df_date[df_date[feat_id] == id]
            if records.empty: total = 0
            else: total = int(records[stat].sum())
            data['dataByFeature'][f'{name}_{id}'].append(total)
    print("Done running data by shelter")
            
    return data



def process_data_for_analysis(df):
    # given the complete dataset, prep it for analysis
    # want by date
    data = {}

    # data ideas
    # 1. Daily service users, average per
    # 2. Daily shelters in use (IDs)
    # 3. Daily organizations in use (IDs)
    # 4. Daily total open beds, average per
    # 5. Daily total open rooms, average per 
    # 6. Group by overnight_service_type
    # 7. Group by program
    # 8. Group by organization

    """
    data = {
        occupancy_date: {
            active_shelters: num;
            active_organizations: num;
            active_programs: num;

            service_users_by_shelter:
                "shelter id" + "shelter name": number -> []
        }
    }
    """
    #'OCCUPANCY_DATE', 'ORGANIZATION_NAME', 'ORGANIZATION_ID', 'SHELTER_ID', 'SHELTER_GROUP', 'LOCATION_NAME', 'LOCATION_ID', 'LOCATION_ADDRESS', 
    #'LOCATION_POSTAL_CODE', 'PROGRAM_ID', 'PROGRAM_NAME', 'PROGRAM_MODEL', 'SECTOR', 'OVERNIGHT_SERVICE_TYPE', 'SERVICE_USER_COUNT', 
    #'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'UNAVAILABLE_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS'
    for date in df['OCCUPANCY_DATE'].unique(): 
        df_data = df[df['OCCUPANCY_DATE'] == date] # all entries with service_user_count across the city

        data[date] = {
            'active_shelters_count': None,
            'active_programs_count': None,
            'active_organizations_count': None,
            'service_users_by_shelters': {},
            'service_users_by_orgs': {},
            'service_users_by_programs': {},
            'occupied_beds_by_shelters': {},
            'occupied_beds_by_orgs': {},
            'occupied_beds_by_programs': {},
            'occupied_rooms_by_shelters': {},
            'occupied_rooms_by_orgs': {},
            'occupied_rooms_by_programs': {},
            'unoccupied_beds_by_shelters': {},
            'unoccupied_beds_by_orgs': {},
            'unoccupied_beds_by_programs': {},
            'unoccupied_rooms_by_shelters': {},
            'unoccupied_rooms_by_orgs': {},
            'unoccupied_rooms_by_programs': {},
        }
        active_shelters = set_counts('SHELTER_ID', 'shelters', data, df_data, date)
        active_orgs = set_counts('ORGANIZATION_ID', 'orgs', data, df_data, date)
        active_programs = set_counts('PROGRAM_ID', 'programs', data, df_data, date)

        set_grouping('SERVICE_USER_COUNT', 'SHELTER_ID', 'SHELTER_GROUP', 'shelters', 'service_users', active_shelters, data, df_data, date)
        set_grouping('SERVICE_USER_COUNT', 'ORGANIZATION_ID', 'ORGANIZATION_NAME', 'orgs', 'service_users', active_orgs, data, df_data, date)
        set_grouping('SERVICE_USER_COUNT', 'PROGRAM_ID', 'PROGRAM_NAME', 'programs', 'service_users', active_programs, data, df_data, date)

        set_grouping('OCCUPIED_BEDS', 'SHELTER_ID', 'SHELTER_GROUP', 'shelters', 'occupied_beds', active_shelters, data, df_data, date)
        set_grouping('OCCUPIED_BEDS', 'ORGANIZATION_ID', 'ORGANIZATION_NAME', 'orgs', 'occupied_beds', active_orgs, data, df_data, date)
        set_grouping('OCCUPIED_BEDS', 'PROGRAM_ID', 'PROGRAM_NAME', 'programs', 'occupied_beds', active_programs, data, df_data, date)

        set_grouping('OCCUPIED_ROOMS', 'SHELTER_ID', 'SHELTER_GROUP', 'shelters', 'occupied_rooms', active_shelters, data, df_data, date)
        set_grouping('OCCUPIED_ROOMS', 'ORGANIZATION_ID', 'ORGANIZATION_NAME', 'orgs', 'occupied_rooms', active_orgs, data, df_data, date)
        set_grouping('OCCUPIED_ROOMS', 'PROGRAM_ID', 'PROGRAM_NAME', 'programs', 'occupied_rooms', active_programs, data, df_data, date)

        set_grouping('UNOCCUPIED_BEDS', 'SHELTER_ID', 'SHELTER_GROUP', 'shelters', 'unoccupied_beds', active_shelters, data, df_data, date)
        set_grouping('UNOCCUPIED_BEDS', 'ORGANIZATION_ID', 'ORGANIZATION_NAME', 'orgs', 'unoccupied_beds', active_orgs, data, df_data, date)
        set_grouping('UNOCCUPIED_BEDS', 'PROGRAM_ID', 'PROGRAM_NAME', 'programs', 'unoccupied_beds', active_programs, data, df_data, date)

        set_grouping('UNOCCUPIED_ROOMS', 'SHELTER_ID', 'SHELTER_GROUP', 'shelters', 'unoccupied_rooms', active_shelters, data, df_data, date)
        set_grouping('UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'ORGANIZATION_NAME', 'orgs', 'unoccupied_rooms', active_orgs, data, df_data, date)
        set_grouping('UNOCCUPIED_ROOMS', 'PROGRAM_ID', 'PROGRAM_NAME', 'programs', 'unoccupied_rooms', active_programs, data, df_data, date)

        # by postal code

    return data

def set_counts(id_key, data_group_key, data, df, date):
    active_ids = df[id_key].unique()
    data[date][f'active_{data_group_key}_count'] = len(active_ids)
    return active_ids

def set_grouping(stat, id_key, name_key, data_group_key, data_stat_key, active_ids, data, df, date):
    for id in active_ids:
        df_filtered = df[df[id_key] == id]
        name = '/'.join([n for n in df_filtered[name_key].unique()])

        data[date][f'{data_stat_key}_by_{data_group_key}'][f'{name} ({id})'] = int(df_filtered[stat].sum())
        

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

# TODO: Optimize with vectorization, built-in pandas functions
@app.get("/data/all/{feature}/{stat}")
async def get_analyze_data(feature: str, stat: str):
    stat_options = ['SERVICE_USER_COUNT', 'OCCUPIED_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_BEDS', 'UNOCCUPIED_ROOMS']
    if stat not in stat_options: return {'message': 'Fail with wrong feature/stat', 'data': {}}

    df = get_data([])
    data = None
    if feature == 'shelters':
        feature_id = 'SHELTER_ID'
        feature_name = 'SHELTER_GROUP'
        data = data_by_feature(df, stat, feature_id, feature_name)
    #processed_data = process_data_for_analysis(data)
    payload = {
        'message': 'Successful retrieval of feature data',
        'data': data
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
    if not data: return {'message': f'Failed FSA data request for {fsa_code}', 'data': {}}
    
    payload = {
        'message': f'Successful FSA data request',
        'data': data,
    }
    return payload

@app.get("/data/nb/{neighbourhood}")
async def data_by_fsa(neighbourhood: str):
    print("Received neighbourhood:", neighbourhood)

    return {'message': 'No data available for neighbourhoods', 'data': {}}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True) # run the server manually