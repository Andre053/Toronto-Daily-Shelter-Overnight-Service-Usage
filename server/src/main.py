import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

import api_setup as setupreq
import api_utilities as utils
import req_geo as georeq
import req_timeseries as tsreq
import req_fsa as fsareq
import req_all as allreq

origins = [
    "http://localhost:8080",
    "http://localhost",
    "http://localhost:3000"
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    payload = {
        'message': 'Root has nothing for you.',
        'data': {}
    }
    return payload

@app.get("/geodata/shelteraddresses")
async def get_shelter_addresses(start: str = None, end: str = None):
    if not utils.validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')

    print('Getting shelter addresses')
    df = setupreq.get_data(['LOCATION_ADDRESS', 'SHELTER_ID', 'SHELTER_NAME'], start, end)
    data = georeq.get_shelter_locations(df)

    return {'message': 'Retrieved shelter locations', 'data': data}    

@app.get("/geodata/{geotype}")
async def get_geo_data(geotype: str): # no date filter needed for geo data

    geojson = georeq.get_geojson_data(geotype)
    payload = {
        'message': 'GeoJson data retrieved',
        'data': geojson
    }
    return payload

@app.get("/data/nb/{neighbourhood}")
async def data_by_fsa(neighbourhood: str):
    return {'message': 'No data available for neighbourhoods', 'data': {}}

@app.get('/data/refresh')
async def refresh():
    utils.download_all_data_csv()

@app.get('/data/timeseries/{freq}/{stat}')
async def get_data_timeseries(freq: str, stat: str, start: str = None, end: str = None):
    if not utils.validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')

    df = setupreq.get_data([], start, end)
    data = None
    if stat in ['SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS']:
        if freq == 'DAILY': data = tsreq.data_timeseries_daily(df, stat)
        elif freq == 'MONTHLY': data = tsreq.data_timeseries_monthly(df, stat)
        elif freq == 'YEARLY': data = tsreq.data_timeseries_yearly(df, stat)

    elif stat in ['ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']: # do not average
        print("This stat must be implemented differently")
        return {}
    
    return {'Message': 'Request to date timeseries completed', 'data': data}

@app.get('/data/all/{timespan}')
async def get_data_by_month(timespan: str, start: str = None, end: str = None):
    if not utils.validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')
    df = setupreq.get_data([], start, end)
    
    if timespan == 'daily': data = allreq.data_all_daily(df)
    elif timespan == 'monthly': data = allreq.data_all_monthly(df)
    elif timespan == 'yearly': data = allreq.data_all_yearly(df)
    elif timespan == 'all': data = allreq.data_all(df)

    payload = {
        'message': 'Retrieved data by month',
        'data': data
    }
    return payload

@app.get('/data/fsa/all')
async def get_data_by_month(start: str = None, end: str = None):
    if not utils.validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')
    df = setupreq.get_data([], start, end)

    data = fsareq.data_all_fsa(df)
    payload = {
        'message': 'Retrieved data by fsa overall',
        'data': data
    }
    return payload

@app.get('/data/fsa/monthly')
async def get_data_by_month(start: str = None, end: str = None):
    if not utils.validate_dates(start, end): return {'message': f'Invalid start date {start} or end date {end}', 'data': {}}
    else:
        if end: end = datetime.strptime(end, '%Y-%m-%d')
        if start: start = datetime.strptime(start, '%Y-%m-%d')
    df = setupreq.get_data([], start, end)

    data = fsareq.data_monthly_fsa(df)
    payload = {
        'message': 'Retrieved data by fsa monthly',
        'data': data
    }
    return payload

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True) # run the server manually