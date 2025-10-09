'''
GLOBALS
- MONTHS

FUNCTIONS
- data_all_yearly()
- data_all_monthly()
- data_all_daily()
- data_all()
'''
import api_resources as ar

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
    
    df = df.fillna(0)
    stats = []

    for idx, row in df.iterrows():
        stats.append({
            'YEAR': idx[0],
            'MONTH': ar.MONTHS[idx[1]],
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