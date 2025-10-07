import pandas as pd
import time

'''
Average
- SERVICE_USER_COUNT
- OCCUPIED_BEDS
- UNOCCUPIED_BEDS
- OCCUPIED ROOMS
- UNOCCUPIED ROOMS
- PROGRAM_ID
- ORGANIZATION_ID
'''

DATA_PATH = "../../data/data_2025.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)
    df['OCCUPANCY_DATE'] = pd.to_datetime(df['OCCUPANCY_DATE'])
    df['LOCATION_FSA_CODE'] = df['LOCATION_POSTAL_CODE'].apply(lambda x: x[:3] if pd.notnull(x) else "N/A")
    return df


# 'OCCUPANCY_DATE', 'ORGANIZATION_NAME', 'ORGANIZATION_ID', 'SHELTER_ID', 'SHELTER_GROUP', 'LOCATION_NAME', 'LOCATION_ID', 'LOCATION_ADDRESS', 'LOCATION_POSTAL_CODE', 'PROGRAM_ID', 'PROGRAM_NAME', 'PROGRAM_MODEL', 'SECTOR', 'OVERNIGHT_SERVICE_TYPE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'UNAVAILABLE_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS'
def stats_by_month():
    print('Called stats by month')
    # data should be tidy
    df = load_data()
    print(df.columns)
    df = df[['OCCUPANCY_DATE', 'LOCATION_FSA_CODE', 'ORGANIZATION_ID', 'SHELTER_ID', 'PROGRAM_ID', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'UNAVAILABLE_BEDS', 'OCCUPIED_ROOMS', 'UNOCCUPIED_ROOMS']]

    data = {}

    # want data by month

    #df_by_month = df.groupby(df['OCCUPANCY_DATE'].dt.month)
    #print(df_by_month.head())
    orgs_by_month = df[['OCCUPANCY_DATE', 'ORGANIZATION_ID', 'LOCATION_FSA_CODE']].groupby([df['OCCUPANCY_DATE'].dt.month, 'LOCATION_FSA_CODE']).agg({
        'ORGANIZATION_ID': 'nunique',
    })
    print(orgs_by_month)

    data['orgCountByMonthByFsa'] = orgs_by_month.to_dict()

    # can make into parquet

def df_to_parquet(df):
    return df.to_parquet()


def main():
    print("Testing from main")
    start = time.perf_counter()
    stats_by_month()
    end = time.perf_counter()

    print(f"Started at {start} and ended at {end} with {end-start} elapsed time.")

if __name__ == '__main__':
    main()