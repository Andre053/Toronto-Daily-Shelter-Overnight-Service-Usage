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
async def get_map_data(filter_type: str, end: str = None, start: str = None):
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






def data_overall(df):
    stats = []

    # multiIndex dataFrame
    print(len(df))
    grouped_fsa = df[
        ['LOCATION_FSA_CODE', 'OCCUPANCY_DATE', 'SERVICE_USER_COUNT', 'CAPACITY_ACTUAL_BED', 
         'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS', 'UNOCCUPIED_BEDS', 'OCCUPIED_ROOMS', 
         'UNOCCUPIED_ROOMS', 'ORGANIZATION_ID', 'PROGRAM_ID', 'SHELTER_ID', 'LOCATION_ID']
        ].groupby(
            ['LOCATION_FSA_CODE'] # already grouped
        ).agg(
            SERVICE_USER_COUNT_MEAN=pd.NamedAgg(
                column='SERVICE_USER_COUNT', 
                aggfunc='mean'
            ),
            SERVICE_USER_COUNT_MAX=pd.NamedAgg(
                column='SERVICE_USER_COUNT', 
                aggfunc='max'
            ),
            SERVICE_USER_COUNT_MIN=pd.NamedAgg(
                column='SERVICE_USER_COUNT', 
                aggfunc='min'
            ),
            CAPACITY_ACTUAL_BED_MEAN=pd.NamedAgg(
                column='CAPACITY_ACTUAL_BED', 
                aggfunc='mean'
            ),
            CAPACITY_ACTUAL_BED_MAX=pd.NamedAgg(
                column='CAPACITY_ACTUAL_BED', 
                aggfunc='max'
            ),
            CAPACITY_ACTUAL_BED_MIN=pd.NamedAgg(
                column='CAPACITY_ACTUAL_BED', 
                aggfunc='min'
            ),
            CAPACITY_FUNDING_BED_MEAN=pd.NamedAgg(
                column='CAPACITY_FUNDING_BED', 
                aggfunc=lambda x: round(x.astype(float).mean(), 2)
            ),
            CAPACITY_FUNDING_BED_MAX=pd.NamedAgg(
                column='CAPACITY_FUNDING_BED', 
                aggfunc='max'
            ),
            CAPACITY_FUNDING_BED_MIN=pd.NamedAgg(
                column='CAPACITY_FUNDING_BED', 
                aggfunc='min'
            ),
            OCCUPIED_ROOMS_MEAN=pd.NamedAgg(
                column='OCCUPIED_ROOMS', 
                aggfunc=lambda x: round(x.astype(float).mean(), 2)
            ),
            OCCUPIED_ROOMS_MAX=pd.NamedAgg(
                column='OCCUPIED_BEDS', 
                aggfunc='max'
            ),
            OCCUPIED_ROOMS_MIN=pd.NamedAgg(
                column='OCCUPIED_BEDS', 
                aggfunc='min'
            ),
            UNOCCUPIED_ROOMS_MEAN=pd.NamedAgg(
                column='UNOCCUPIED_ROOMS', 
                aggfunc=lambda x: round(x.astype(float).mean(), 2)
            ),
            UNOCCUPIED_ROOMS_MAX=pd.NamedAgg(
                column='UNOCCUPIED_BEDS', 
                aggfunc='max'
            ),
            UNOCCUPIED_ROOMS_MIN=pd.NamedAgg(
                column='UNOCCUPIED_BEDS', 
                aggfunc='min'
            ),
            OCCUPIED_BEDS_MEAN=pd.NamedAgg(
                column='OCCUPIED_BEDS', 
                aggfunc=lambda x: round(x.astype(float).mean(), 2)
            ),
            OCCUPIED_BEDS_MAX=pd.NamedAgg(
                column='OCCUPIED_ROOMS', 
                aggfunc='max'
            ),
            OCCUPIED_BEDS_MIN=pd.NamedAgg(
                column='OCCUPIED_ROOMS', 
                aggfunc='min'
            ),
            UNOCCUPIED_BEDS_MEAN=pd.NamedAgg(
                column='UNOCCUPIED_BEDS', 
                aggfunc=lambda x: round(x.astype(float).mean(), 2)
            ),
            UNOCCUPIED_BEDS_MAX=pd.NamedAgg(
                column='UNOCCUPIED_ROOMS', 
                aggfunc='max'
            ),
            UNOCCUPIED_BEDS_MIN=pd.NamedAgg(
                column='UNOCCUPIED_ROOMS', 
                aggfunc='min'
            ),
            ORG_COUNT=pd.NamedAgg(
                column='ORGANIZATION_ID', 
                aggfunc='nunique'
            ),
            PROGRAM_COUNT=pd.NamedAgg(
                column='PROGRAM_ID', 
                aggfunc='nunique'
            ),
            SHELTER_COUNT=pd.NamedAgg(
                column='SHELTER_ID', 
                aggfunc='nunique'
            ),
            LOCATION_COUNT=pd.NamedAgg(
                column='LOCATION_ID', 
                aggfunc='nunique'
            ),
    )
    grouped_fsa.columns = ['SERVICE_USER_COUNT_MEAN', 'SERVICE_USER_COUNT_MAX',
                        'SERVICE_USER_COUNT_MIN', 'CAPACITY_ACTUAL_BED', 'CAPACITY_FUNDING_BED', 'OCCUPIED_BEDS_MEAN',
                        'UNOCCUPIED_BEDS_MEAN', 'OCCUPIED_ROOMS_MEAN', 'UNOCCUPIED_ROOMS_MEAN', 'ORG_COUNT', 
                        'PROGRAM_COUNT', 'SHELTER_COUNT', 'LOCATION_COUNT',
                        'OCCUPIED_BEDS_MAX', 'OCCUPIED_BEDS_MIN', 'OCCUPIED_ROOMS_MAX', 'OCCUPIED_ROOMS_MIN',
                        'UNOCCUPIED_BEDS_MAX', 'UNOCCUPIED_BEDS_MIN', 'UNOCCUPIED_ROOMS_MAX', 'UNOCCUPIED_ROOMS_MIN',
                        'CAPACITY_ACTUAL_BED_MAX', 'CAPACITY_ACTUAL_BED_MIN', 'CAPACITY_FUNDING_BED_MAX', 'CAPACITY_FUNDING_BED_MIN']
    print(grouped_fsa)
    grouped_fsa = grouped_fsa.fillna(0)
    for key, group in grouped_fsa.groupby('LOCATION_FSA_CODE'):
        group_data = group.iloc[0]

        stats.append({
            'FSA': key,
            'STATS':  {
                'MEAN_SERVICE_USERS': group_data['SERVICE_USER_COUNT_MEAN'],
                'MAX_SERVICE_USERS': group_data['SERVICE_USER_COUNT_MAX'],
                'MIN_SERVICE_USERS': group_data['SERVICE_USER_COUNT_MIN'],
                'MEAN_CAPACITY_ACTUAL_BED': group_data['CAPACITY_ACTUAL_BED'],
                'MAX_CAPACITY_ACTUAL_BED': group_data['CAPACITY_ACTUAL_BED_MAX'],
                'MIN_CAPACITY_ACTUAL_BED': group_data['CAPACITY_ACTUAL_BED_MIN'],
                'MEAN_CAPACITY_FUNDING_BED': group_data['CAPACITY_FUNDING_BED'],
                'MAX_CAPACITY_FUNDING_BED': group_data['CAPACITY_FUNDING_BED_MAX'],
                'MIN_CAPACITY_FUNDING_BED': group_data['CAPACITY_FUNDING_BED_MIN'],
                'MEAN_OCCUPIED_BEDS': group_data['OCCUPIED_BEDS_MEAN'],
                'MAX_OCCUPIED_BEDS': group_data['OCCUPIED_BEDS_MAX'],
                'MIN_OCCUPIED_BEDS': group_data['OCCUPIED_BEDS_MIN'],
                'MEAN_UNOCCUPIED_BEDS': group_data['UNOCCUPIED_BEDS_MEAN'],
                'MAX_UNOCCUPIED_BEDS': group_data['UNOCCUPIED_BEDS_MAX'],
                'MIN_UNOCCUPIED_BEDS': group_data['UNOCCUPIED_BEDS_MIN'],
                'MEAN_OCCUPIED_ROOMS': group_data['OCCUPIED_ROOMS_MEAN'],
                'MAX_OCCUPIED_ROOMS': group_data['OCCUPIED_ROOMS_MAX'],
                'MIN_OCCUPIED_ROOMS': group_data['OCCUPIED_ROOMS_MIN'],
                'MEAN_UNOCCUPIED_ROOMS': group_data['UNOCCUPIED_ROOMS_MEAN'],
                'MAX_UNOCCUPIED_ROOMS': group_data['UNOCCUPIED_ROOMS_MAX'],
                'MIN_UNOCCUPIED_ROOMS': group_data['UNOCCUPIED_ROOMS_MIN'],
                'MEAN_ORG_COUNT': group_data['ORG_COUNT'],
                'MEAN_PROGRAM_COUNT': group_data['PROGRAM_COUNT'],
                'MEAN_SHELTER_COUNT': group_data['SHELTER_COUNT'],
                'MEAN_LOCATION_COUNT': group_data['LOCATION_COUNT']
            }})
    return stats