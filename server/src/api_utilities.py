'''
FUNCTIONS
- fill_stats
- find_lat_long
- validate_dates
- validate_date
'''
import pandas as pd
from datetime import datetime

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