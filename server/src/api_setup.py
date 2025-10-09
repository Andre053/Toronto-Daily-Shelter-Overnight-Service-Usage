'''
GLOBALS
- DATA_PATH
- DATA_FOLDER
- GLOBALS_PATH

FUNCTIONS
- get_data()
- download_all_data_csv(): Used everyday to get up-to-date daily data
    - Downloads all data from Open Data Toronto and saves the files
    - The files are yearly, so if the previous old files are already downloaded, they are skipped
    - The entire 2025 file is downloaded each new day
    - TODO: Only add new data to file? Use specific download query
- download_specific_data(): Not currently used
    - Based on Open Data Toronto code on how to retrieve specific data from the db
    - TODO: Try and use to get new daily data everyday
- parse_date()
- prep_data()
- get_last_updated_date()
- set_last_updated_date()
- load_dataframe()
'''
import os, json, glob
import pandas as pd
import requests as req

from urllib.request import urlretrieve
from pathlib import Path
from datetime import datetime

import api_resources as ar
# filter dataframe based on list of columns
def get_data(col_filter, start=None, end=None):
    df = load_dataframe()
    df = prep_data(df, start, end)

    if col_filter: return df[col_filter]
    return df

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
    with open(ar.GLOBALS_PATH, 'r') as f:
        data = json.load(f)
        return data['DATA_LAST_UPDATED']

def set_last_updated_date():
    current_date = datetime.now().strftime('%Y/%m/%d')
    data = {'DATA_LAST_UPDATED': f'{current_date}'}
    with open(ar.GLOBALS_PATH, 'w') as f:
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
    df_list = [pd.read_csv(path, usecols=use_cols) for path in glob.glob(f'{ar.DATA_FOLDER}/data_*.csv')]
    df = pd.concat(df_list)

    return df