import json, uvicorn, os, glob
import pandas as pd
import numpy as np
import requests as req

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from urllib.request import urlretrieve
from datetime import datetime, timedelta
from pathlib import Path
#from data_utilities import data_analysis

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
DATA_FOLDER = "../data"
GEOJSON_FSA_PATH = "../data/GeoJson/tor_fsa_cbf.geojson"
GEOJSON_NB_PATH = "../data/GeoJson/tor_neighbourhoods.geojson"

MONTHS = {
    1: 'JAN',
    2: 'FEB',
    3: 'MAR',
    4: 'APR',
    5: 'MAY',
    6: 'JUN',
    7: 'JUL',
    8: 'AUG',
    9: 'SEP',
    10: 'OCT',
    11: 'NOV',
    12: 'DEC',
}

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

def download_all_data_csv():
    BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    PACKAGE = "daily-shelter-overnight-service-occupancy-capacity"

    url = BASE_URL + "/api/3/action/package_show"
    params = {"id": PACKAGE}

    dir = os.getcwd()

    package = req.get(url, params=params).json()

    package_name_2025 = 'Daily shelter overnight occupancy'
    older_packages = [
        'daily-shelter-overnight-service-occupancy-capacity-2024',
        'daily-shelter-overnight-service-occupancy-capacity-2023',
        'daily-shelter-overnight-service-occupancy-capacity-2022',
        'daily-shelter-overnight-service-occupancy-capacity-2021'
    ]
    for i, resource in enumerate(package['result']['resources']): # we need to update the 2025 one, others only need to be downloaded once
        if resource['datastore_active']:
            # get 2025 records in CSV
            url = BASE_URL + '/api/3/action/resource_show?id=' + resource['id']
            metadata = req.get(url).json()
            if metadata and metadata['result']['name'] == package_name_2025: # must update most recent year
                url = BASE_URL + '/datastore/dump/' + resource['id']
                path = f"../data/data_2025.csv"
                filename = os.path.join(dir, path)
                urlretrieve(url=url, filename=filename)
            elif metadata and metadata['result']['name'] in older_packages:
                year = metadata['result']['name'][-4:]
                path = f"../data/data_{year}.csv"
                if not Path(path).exists(): # only download once
                    url = BASE_URL + '/datastore/dump/' + resource['id']
                    filename = os.path.join(dir, path)
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

def parse_date(date):
    date_length = len(date)

    # dates must be in %Y-%m-%d form, some had T00:00:00 appended or were %y at start
    if pd.isna(date): return None
    if date_length == 19: date = date[:-9]
    elif date_length == 8: date = '20' + date
    else: return date

    return date

def prep_data(df, start=None, end=None):
    #df['OCCUPANCY_DATE'] = parse_date(df['OCCUPANCY_DATE']) # vectorize solution
    df['OCCUPANCY_DATE'] = df['OCCUPANCY_DATE'].apply(lambda x: parse_date(x)) # 
    df['OCCUPANCY_DATE'] = pd.to_datetime(df['OCCUPANCY_DATE'], format='%Y-%m-%d')
    df['LOCATION_FSA_CODE'] = df['LOCATION_POSTAL_CODE'].apply(lambda x: x[:3] if pd.notnull(x) else "N/A")
    #df = df.fillna(None) # 0 would have been being counted

    if (start and end):
        mask = (df['OCCUPANCY_DATE'] > start) & (df['OCCUPANCY_DATE'] < end)
        print('Applying start and end mask')
        return df.loc[mask]
    elif (start):
        mask = (df['OCCUPANCY_DATE'] > start)
        print('Applying start mask')
        return df.loc[mask]
    elif (end): 
        mask = (df['OCCUPANCY_DATE'] < end)
        print('Applying end mask')
        return df.loc[mask]
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

    # there are multiple csvs
    use_cols = ['OCCUPANCY_DATE', 'ORGANIZATION_NAME', 'ORGANIZATION_ID', 'SHELTER_ID', 'SHELTER_GROUP', 'LOCATION_NAME', 'LOCATION_ID', 'LOCATION_ADDRESS', 'LOCATION_POSTAL_CODE', 'PROGRAM_ID', 'PROGRAM_NAME', 'PROGRAM_MODEL', 'SECTOR', 'OVERNIGHT_SERVICE_TYPE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'UNAVAILABLE_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS']
    df_list = [pd.read_csv(path, usecols=use_cols) for path in glob.glob(f'{DATA_FOLDER}/data_*.csv')]
    df = pd.concat(df_list)

    return df


# filter dataframe based on list of columns
def get_data(col_filter, start=None, end=None):
    df = load_dataframe()
    df = prep_data(df, start, end)

    if col_filter: return df[col_filter]
    return df


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
    
@app.get("/")
async def root():
    download_all_data_csv()
    payload = {
        'message': 'Root has no data to give',
        'data': {}
    }
    return payload


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

@app.get("/geodata/shelteraddresses")
async def get_shelter_addresses(start: str = None, end: str = None):
    if not validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')

    print('Getting shelter addresses')
    df = get_data([], start, end)
    data = find_lat_lon(df['LOCATION_ADDRESS'].unique())

    return {'message': 'Retrieved shelter locations', 'data': data}    

@app.get("/geodata/{geotype}")
async def get_geo_data(geotype: str): # no date filter needed for geo data

    geojson = get_geojson_data(geotype)
    payload = {
        'message': 'GeoJson data retrieved',
        'data': geojson
    }
    return payload

@app.get("/data/nb/{neighbourhood}")
async def data_by_fsa(neighbourhood: str):
    return {'message': 'No data available for neighbourhoods', 'data': {}}

# make the data_xxx into a single function
group_by_aggregate = {
    'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
    'OCCUPIED_BEDS': ['mean', 'max', 'min'],
    'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
    'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
    'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
    'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
    'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
    'PROGRAM_ID': 'nunique',
    'SHELTER_ID': 'nunique',
    'LOCATION_ID': 'nunique',
    'ORGANIZATION_ID': 'nunique',
}

def fill_stats(row):
    return {
        'MEAN_SERVICE_USERS': row['SERVICE_USER_COUNT']['mean'],
        'MAX_SERVICE_USERS': row['SERVICE_USER_COUNT']['max'],
        'MIN_SERVICE_USERS': row['SERVICE_USER_COUNT']['min'],
        'MEAN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['mean'],
        'MAX_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['max'],
        'MIN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['min'],
        'MEAN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['mean'],
        'MAX_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['max'],
        'MIN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['min'],
        'MEAN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['mean'],
        'MAX_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['max'],
        'MIN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['min'],
        'MEAN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['mean'],
        'MAX_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['max'],
        'MIN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['min'],
        'MEAN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['mean'],
        'MAX_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['max'],
        'MIN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['min'],
        'MEAN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['mean'],
        'MAX_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['max'],
        'MIN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['min'],
        'UNIQUE_ORG_COUNT': row['ORGANIZATION_ID']['nunique'],
        'UNIQUE_PROGRAM_COUNT': row['PROGRAM_ID']['nunique'],
        'UNIQUE_SHELTER_COUNT': row['SHELTER_ID']['nunique'],
        'UNIQUE_LOCATION_COUNT': row['LOCATION_ID']['nunique']
    }

def data_yearly(df):
    grouped_fsa = df[
        ['LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR')
            ]).agg(group_by_aggregate).reset_index()
    
    grouped_fsa = grouped_fsa.fillna(0)
    stats = []

    for idx, row in grouped_fsa.iterrows():
        stats.append({
            'YEAR': row['YEAR'][''],
            'STATS':  fill_stats(row)
        })
    return stats

def data_monthly(df):
    grouped_fsa = df[
        ['LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR'),
                df['OCCUPANCY_DATE'].dt.month.rename('MONTH')
            ]).agg(group_by_aggregate).reset_index()
    
    grouped_fsa = grouped_fsa.fillna(0)
    stats = []

    for idx, row in grouped_fsa.iterrows():
        stats.append({
            'YEAR': row['YEAR'][''],
            'MONTH': MONTHS[row['MONTH']['']],
            'STATS':  fill_stats(row)
        })
    return stats

def data_monthly_fsa(df):
    grouped_fsa = df[
        ['LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR'),
                df['OCCUPANCY_DATE'].dt.month.rename('MONTH'),
                'LOCATION_FSA_CODE'
            ]).agg(group_by_aggregate).reset_index()
    
    grouped_fsa = grouped_fsa.fillna(0)
    stats = []

    for idx, row in grouped_fsa.iterrows():
        stats.append({
            'YEAR': row['YEAR'][''],
            'MONTH': MONTHS[row['MONTH']['']],
            'FSA': row['LOCATION_FSA_CODE'][''],
            'STATS':  fill_stats(row)
        })
    return stats


#'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID'
def data_timeseries_yearly(df, stat):
    df = df[
        ['OCCUPANCY_DATE', stat]
        ].groupby([
                'OCCUPANCY_DATE',
                df['OCCUPANCY_DATE'].dt.month.rename('MONTH'),
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR')
            ]).agg({
                stat: 'sum',
            })
    
    df = df.groupby(['YEAR', 'MONTH']).agg({
                stat: 'mean',
            })
    df = df.groupby(['YEAR']).agg({
                stat: 'mean',
            }).round(2)
    df = df.fillna(0)
    dataPoints = []
    for idx, row in df.iterrows():
        dataPoints.append({
            'DATE': datetime(idx, 1, 1),
            'STAT': int(row[stat])
        })
    return {
        'timespan': 'yearly',
        'max': int(df.max()[stat]),
        'min': int(df.min()[stat]),
        'dataPoints': dataPoints
    }
# get daily sum, then monthly average
def data_timeseries_monthly(df, stat):
    df = df[
        ['OCCUPANCY_DATE', stat]
        ].groupby([
                'OCCUPANCY_DATE',
                df['OCCUPANCY_DATE'].dt.month.rename('MONTH'),
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR')
            ]).agg({
                stat: 'sum',
            })
    
    df = df.groupby(['YEAR', 'MONTH']).agg({
                stat: 'mean',
            }).round(2)
    df = df.fillna(0)
    dataPoints = []
    for idx, row in df.iterrows():
        dataPoints.append({
            'DATE': datetime(idx[0], idx[1], 1),
            'STAT': int(row[stat])
        })
    return {
        'timespan': 'monthly',
        'max': int(df.max()[stat]),
        'min': int(df.min()[stat]),
        'dataPoints': dataPoints
    }

def data_timeseries_daily(df, stat):
    df = df[
        ['OCCUPANCY_DATE', stat]
        ].groupby([
                'OCCUPANCY_DATE'
            ]).agg({
                stat: 'sum',
            })
    df = df.fillna(0)
    dataPoints = []
    for idx, row in df.iterrows():
        dataPoints.append({
            'DATE': idx,
            'STAT': int(row[stat])
        })
    return {
        'timespan': 'daily',
        'max': int(df.max()[stat]),
        'min': int(df.min()[stat]),
        'dataPoints': dataPoints
    }

def data_all_single_fsa(df, fsa_code):
    df = df[df['LOCATION_FSA_CODE'] == fsa_code]
    grouped = df[
        ['LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby('LOCATION_FSA_CODE').agg(group_by_aggregate).reset_index()
    grouped = grouped.fillna(0)
    stats = []
    for idx, row in grouped.iterrows():
        stats.append({
            'FSA': row['LOCATION_FSA_CODE'][''],
            'STATS':  fill_stats(row)
        })
    return stats

# THIS IS DONE
def data_all_fsa(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                'LOCATION_FSA_CODE',
                'OCCUPANCY_DATE'
            ]).agg({
                'SERVICE_USER_COUNT': 'sum',
                'OCCUPIED_BEDS': 'sum',
                'UNOCCUPIED_BEDS': 'sum',
                'OCCUPIED_ROOMS': 'sum',
                'UNOCCUPIED_ROOMS': 'sum',
                'CAPACITY_ACTUAL_BED': 'sum',
                'CAPACITY_FUNDING_BED': 'sum',
                'PROGRAM_ID': 'nunique',
                'SHELTER_ID': 'nunique',
                'LOCATION_ID': 'nunique',
                'ORGANIZATION_ID': 'nunique',
            })
    
    df = df.groupby('LOCATION_FSA_CODE').agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            }).round(2)
    df = df.fillna(0)
    stats = []

    for idx, row in df.iterrows():
        stats.append({
            'FSA': idx,
            'STATS':  {
                'MEAN_SERVICE_USERS': row['SERVICE_USER_COUNT']['mean'],
                'MAX_SERVICE_USERS': row['SERVICE_USER_COUNT']['max'],
                'MIN_SERVICE_USERS': row['SERVICE_USER_COUNT']['min'],
                'MEAN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['mean'],
                'MAX_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['max'],
                'MIN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['min'],
                'MEAN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['mean'],
                'MAX_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['max'],
                'MIN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['min'],
                'MEAN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['mean'],
                'MAX_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['max'],
                'MIN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['min'],
                'MEAN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['mean'],
                'MAX_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['max'],
                'MIN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['min'],
                'MEAN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['mean'],
                'MAX_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['max'],
                'MIN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['min'],
                'MEAN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['mean'],
                'MAX_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['max'],
                'MIN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['min'],
                'UNIQUE_ORG_COUNT': row['ORGANIZATION_ID']['mean'],
                'UNIQUE_PROGRAM_COUNT': row['PROGRAM_ID']['mean'],
                'UNIQUE_SHELTER_COUNT': row['SHELTER_ID']['mean'],
                'UNIQUE_LOCATION_COUNT': row['LOCATION_ID']['mean']
            }
        })
    return stats

def data_all_yearly(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                'OCCUPANCY_DATE',
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR')
            ]).agg({
                'SERVICE_USER_COUNT': 'sum',
                'OCCUPIED_BEDS': 'sum',
                'UNOCCUPIED_BEDS': 'sum',
                'OCCUPIED_ROOMS': 'sum',
                'UNOCCUPIED_ROOMS': 'sum',
                'CAPACITY_ACTUAL_BED': 'sum',
                'CAPACITY_FUNDING_BED': 'sum',
                'PROGRAM_ID': 'nunique',
                'SHELTER_ID': 'nunique',
                'LOCATION_ID': 'nunique',
                'ORGANIZATION_ID': 'nunique',
            })
    
    print(df.head())
    df = df.groupby(['YEAR']).agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            }).round(2)
    
    print(df.head())

    df = df.fillna(0)
    stats = []

    for idx, row in df.iterrows():
        stats.append({
            'YEAR': idx,
            'STATS':  {
                'MEAN_SERVICE_USERS': row['SERVICE_USER_COUNT']['mean'],
                'MAX_SERVICE_USERS': row['SERVICE_USER_COUNT']['max'],
                'MIN_SERVICE_USERS': row['SERVICE_USER_COUNT']['min'],
                'MEAN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['mean'],
                'MAX_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['max'],
                'MIN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['min'],
                'MEAN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['mean'],
                'MAX_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['max'],
                'MIN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['min'],
                'MEAN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['mean'],
                'MAX_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['max'],
                'MIN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['min'],
                'MEAN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['mean'],
                'MAX_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['max'],
                'MIN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['min'],
                'MEAN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['mean'],
                'MAX_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['max'],
                'MIN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['min'],
                'MEAN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['mean'],
                'MAX_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['max'],
                'MIN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['min'],
                'UNIQUE_ORG_COUNT': row['ORGANIZATION_ID']['mean'],
                'UNIQUE_PROGRAM_COUNT': row['PROGRAM_ID']['mean'],
                'UNIQUE_SHELTER_COUNT': row['SHELTER_ID']['mean'],
                'UNIQUE_LOCATION_COUNT': row['LOCATION_ID']['mean']
            }
        })
    return stats

# DONE
def data_all_monthly(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                'OCCUPANCY_DATE',
                df['OCCUPANCY_DATE'].dt.month.rename('MONTH'),
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR')
            ]).agg({
                'SERVICE_USER_COUNT': 'sum',
                'OCCUPIED_BEDS': 'sum',
                'UNOCCUPIED_BEDS': 'sum',
                'OCCUPIED_ROOMS': 'sum',
                'UNOCCUPIED_ROOMS': 'sum',
                'CAPACITY_ACTUAL_BED': 'sum',
                'CAPACITY_FUNDING_BED': 'sum',
                'PROGRAM_ID': 'nunique',
                'SHELTER_ID': 'nunique',
                'LOCATION_ID': 'nunique',
                'ORGANIZATION_ID': 'nunique',
            })
    
    print(df.head())
    df = df.groupby(['YEAR', 'MONTH']).agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            }).round(2)
    
    print(df.head())

    df = df.fillna(0)
    stats = []

    for idx, row in df.iterrows():
        stats.append({
            'YEAR': idx[0],
            'MONTH': MONTHS[idx[1]],
            'STATS':  {
                'MEAN_SERVICE_USERS': row['SERVICE_USER_COUNT']['mean'],
                'MAX_SERVICE_USERS': row['SERVICE_USER_COUNT']['max'],
                'MIN_SERVICE_USERS': row['SERVICE_USER_COUNT']['min'],
                'MEAN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['mean'],
                'MAX_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['max'],
                'MIN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['min'],
                'MEAN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['mean'],
                'MAX_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['max'],
                'MIN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['min'],
                'MEAN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['mean'],
                'MAX_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['max'],
                'MIN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['min'],
                'MEAN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['mean'],
                'MAX_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['max'],
                'MIN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['min'],
                'MEAN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['mean'],
                'MAX_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['max'],
                'MIN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['min'],
                'MEAN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['mean'],
                'MAX_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['max'],
                'MIN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['min'],
                'UNIQUE_ORG_COUNT': row['ORGANIZATION_ID']['mean'],
                'UNIQUE_PROGRAM_COUNT': row['PROGRAM_ID']['mean'],
                'UNIQUE_SHELTER_COUNT': row['SHELTER_ID']['mean'],
                'UNIQUE_LOCATION_COUNT': row['LOCATION_ID']['mean']
            }
        })
    return stats

# DONE
def data_all_daily(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby(
                'OCCUPANCY_DATE'
            ).agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            })
    df = df.fillna(0)
    stats = []

    for idx, row in df.iterrows():
        stats.append({
            'DATE': idx,
            'STATS':  {
                'MEAN_SERVICE_USERS': row['SERVICE_USER_COUNT']['mean'],
                'MAX_SERVICE_USERS': row['SERVICE_USER_COUNT']['max'],
                'MIN_SERVICE_USERS': row['SERVICE_USER_COUNT']['min'],
                'MEAN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['mean'],
                'MAX_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['max'],
                'MIN_CAPACITY_ACTUAL_BED': row['CAPACITY_ACTUAL_BED']['min'],
                'MEAN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['mean'],
                'MAX_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['max'],
                'MIN_CAPACITY_FUNDING_BED': row['CAPACITY_FUNDING_BED']['min'],
                'MEAN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['mean'],
                'MAX_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['max'],
                'MIN_OCCUPIED_BEDS': row['OCCUPIED_BEDS']['min'],
                'MEAN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['mean'],
                'MAX_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['max'],
                'MIN_UNOCCUPIED_BEDS': row['UNOCCUPIED_BEDS']['min'],
                'MEAN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['mean'],
                'MAX_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['max'],
                'MIN_OCCUPIED_ROOMS': row['OCCUPIED_ROOMS']['min'],
                'MEAN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['mean'],
                'MAX_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['max'],
                'MIN_UNOCCUPIED_ROOMS': row['UNOCCUPIED_ROOMS']['min'],
                'UNIQUE_ORG_COUNT': row['ORGANIZATION_ID']['mean'],
                'UNIQUE_PROGRAM_COUNT': row['PROGRAM_ID']['mean'],
                'UNIQUE_SHELTER_COUNT': row['SHELTER_ID']['mean'],
                'UNIQUE_LOCATION_COUNT': row['LOCATION_ID']['mean']
            }
        })
    return stats

def data_all(df):
    df = df[
        ['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby(
                'OCCUPANCY_DATE'
            ).agg({
                'SERVICE_USER_COUNT': 'sum',
                'OCCUPIED_BEDS': 'sum',
                'UNOCCUPIED_BEDS': 'sum',
                'OCCUPIED_ROOMS': 'sum',
                'UNOCCUPIED_ROOMS': 'sum',
                'CAPACITY_ACTUAL_BED': 'sum',
                'CAPACITY_FUNDING_BED': 'sum',
                'PROGRAM_ID': 'nunique',
                'SHELTER_ID': 'nunique',
                'LOCATION_ID': 'nunique',
                'ORGANIZATION_ID': 'nunique',
            })
    
    df = df.agg({
                'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
                'OCCUPIED_BEDS': ['mean', 'max', 'min'],
                'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
                'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
                'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
                'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
                'PROGRAM_ID': 'mean',
                'SHELTER_ID': 'mean',
                'LOCATION_ID': 'mean',
                'ORGANIZATION_ID': 'mean',
            }).round(2)
    df = df.fillna(0)
    stats = []

    stats = {
        'STATS':  {
            'MEAN_SERVICE_USERS': df['SERVICE_USER_COUNT']['mean'],
            'MAX_SERVICE_USERS': df['SERVICE_USER_COUNT']['max'],
            'MIN_SERVICE_USERS': df['SERVICE_USER_COUNT']['min'],
            'MEAN_CAPACITY_ACTUAL_BED': df['CAPACITY_ACTUAL_BED']['mean'],
            'MAX_CAPACITY_ACTUAL_BED': df['CAPACITY_ACTUAL_BED']['max'],
            'MIN_CAPACITY_ACTUAL_BED': df['CAPACITY_ACTUAL_BED']['min'],
            'MEAN_CAPACITY_FUNDING_BED': df['CAPACITY_FUNDING_BED']['mean'],
            'MAX_CAPACITY_FUNDING_BED': df['CAPACITY_FUNDING_BED']['max'],
            'MIN_CAPACITY_FUNDING_BED': df['CAPACITY_FUNDING_BED']['min'],
            'MEAN_OCCUPIED_BEDS': df['OCCUPIED_BEDS']['mean'],
            'MAX_OCCUPIED_BEDS': df['OCCUPIED_BEDS']['max'],
            'MIN_OCCUPIED_BEDS': df['OCCUPIED_BEDS']['min'],
            'MEAN_UNOCCUPIED_BEDS': df['UNOCCUPIED_BEDS']['mean'],
            'MAX_UNOCCUPIED_BEDS': df['UNOCCUPIED_BEDS']['max'],
            'MIN_UNOCCUPIED_BEDS': df['UNOCCUPIED_BEDS']['min'],
            'MEAN_OCCUPIED_ROOMS': df['OCCUPIED_ROOMS']['mean'],
            'MAX_OCCUPIED_ROOMS': df['OCCUPIED_ROOMS']['max'],
            'MIN_OCCUPIED_ROOMS': df['OCCUPIED_ROOMS']['min'],
            'MEAN_UNOCCUPIED_ROOMS': df['UNOCCUPIED_ROOMS']['mean'],
            'MAX_UNOCCUPIED_ROOMS': df['UNOCCUPIED_ROOMS']['max'],
            'MIN_UNOCCUPIED_ROOMS': df['UNOCCUPIED_ROOMS']['min'],
            'UNIQUE_ORG_COUNT': df['ORGANIZATION_ID']['mean'],
            'UNIQUE_PROGRAM_COUNT': df['PROGRAM_ID']['mean'],
            'UNIQUE_SHELTER_COUNT': df['SHELTER_ID']['mean'],
            'UNIQUE_LOCATION_COUNT': df['LOCATION_ID']['mean']
        }
    }
    return stats

@app.get('/data/refresh')
async def refresh():
    download_all_data_csv()

def validate_dates(start, end):
    if (end and start):
        if (not validate_date(end) or not validate_date(start)): return False
    elif (start):
        if (not validate_date(start)): return False
    elif (end):
        if (not validate_date(end)): return False
    return True

def validate_date(date):
    format = '%Y-%m-%d'
    start_date = datetime.strptime('2021-01-01', format)
    today = datetime.now() # yesterday's date
    try:
        date = datetime.strptime(date, format)
        if date >= start_date and date < today:
            return True
    except ValueError:
        print('Error with dates')
    return False

# 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID'

@app.get('/data/timeseries/{freq}/{stat}')
async def get_data_timeseries(freq: str, stat: str, start: str = None, end: str = None):
    if not validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')

    df = get_data([], start, end)
    data = None
    if stat in ['SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS']:
        if freq == 'DAILY': data = data_timeseries_daily(df, stat)
        elif freq == 'MONTHLY': data = data_timeseries_monthly(df, stat)
        elif freq == 'YEARLY': data = data_timeseries_yearly(df, stat)

    elif stat in ['ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']: # do not average
        print("This stat must be implemented differently")
        return {}
    
    return {'Message': 'Request to date timeseries completed', 'data': data}
@app.get('/data/all/{timespan}')
async def get_data_by_month(timespan: str, start: str = None, end: str = None):
    if not validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')
    df = get_data([], start, end)

    
    if timespan == 'daily': data = data_all_daily(df)
    elif timespan == 'monthly': data = data_all_monthly(df)
    elif timespan == 'yearly': data = data_all_yearly(df)
    elif timespan == 'all': data = data_all(df)

    payload = {
        'message': 'Retrieved data by month',
        'data': data
    }
    return payload


@app.get('/data/monthly')
async def get_data_by_month(start: str = None, end: str = None):
    if not validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')
    df = get_data([], start, end)

    data = data_monthly(df)
    payload = {
        'message': 'Retrieved data by month',
        'data': data
    }
    return payload



@app.get('/data/fsa/all/{fsa_code}')
async def get_data_by_month_single(fsa_code: str, start: str = None, end: str = None):
    if not validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')
    df = get_data([], start, end)

    data = data_all_single_fsa(df, fsa_code)
    payload = {
        'message': 'Retrieved data by fsa overall',
        'data': data
    }
    return payload

@app.get('/data/fsa/all')
async def get_data_by_month(start: str = None, end: str = None):
    if not validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')
    df = get_data([], start, end)

    data = data_all_fsa(df)
    payload = {
        'message': 'Retrieved data by fsa overall',
        'data': data
    }
    return payload

@app.get('/data/yearly')
async def get_data_by_month(start: str = None, end: str = None):
    if not validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')
    df = get_data([], start, end)

    data = data_yearly(df)
    payload = {
        'message': 'Retrieved data by month',
        'data': data
    }
    return payload

@app.get('/data/fsa/monthly')
async def get_data_by_month(start: str = None, end: str = None):
    if not validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')

    df = get_data([], start, end)

    data = data_monthly_fsa(df)
    payload = {
        'message': 'Retrieved data by fsa monthly',
        'data': data
    }
    return payload

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True) # run the server manually