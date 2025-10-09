'''
FUNCTIONS
- data_timeseries_yearly()
- data_timeseries_monthly()
- data_timeseries_daily()

'''
from datetime import datetime

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
        'stat': stat,
        'timespan': 'yearly',
        'max': int(df.max()[stat]),
        'min': int(df.min()[stat]),
        'dataPoints': dataPoints
    }
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
        'stat': stat,
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
        'stat': stat,
        'timespan': 'daily',
        'max': int(df.max()[stat]),
        'min': int(df.min()[stat]),
        'dataPoints': dataPoints
    }
