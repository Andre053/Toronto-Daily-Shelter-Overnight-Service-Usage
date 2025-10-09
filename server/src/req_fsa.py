'''
GLOBALS
- GROUP_BY_AGGREGATE
- MONTHS

FUNCTIONS
- data_monthly_fsa()
- data_all_single_fsa()

OUTSIDE FUNCTIONS
- fill_stats()
'''

import api_resources as ar

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

def data_monthly_fsa(df):
    grouped_fsa = df[
        ['LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby([
                df['OCCUPANCY_DATE'].dt.year.rename('YEAR'),
                df['OCCUPANCY_DATE'].dt.month.rename('MONTH'),
                'LOCATION_FSA_CODE'
            ]).agg(ar.GROUP_BY_AGGREGATE).reset_index()
    
    grouped_fsa = grouped_fsa.fillna(0)
    stats = []

    for idx, row in grouped_fsa.iterrows():
        stats.append({
            'YEAR': row['YEAR'][''],
            'MONTH': ar.MONTHS[row['MONTH']['']],
            'FSA': row['LOCATION_FSA_CODE'][''],
            'STATS':  ar.fill_stats(row)
        })
    return stats


def data_all_single_fsa(df, fsa_code):
    df = df[df['LOCATION_FSA_CODE'] == fsa_code]
    grouped = df[
        ['LOCATION_FSA_CODE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby('LOCATION_FSA_CODE').agg(ar.GROUP_BY_AGGREGATE).reset_index()
    grouped = grouped.fillna(0)
    stats = []
    for idx, row in grouped.iterrows():
        stats.append({
            'FSA': row['LOCATION_FSA_CODE'][''],
            'STATS':  ar.fill_stats(row)
        })
    return stats