import numpy as np
from datetime import datetime as dt

def payment_parser(data):

    asset_classification_map = {'N': 'XXX', '?': 'XXX', '0': 'DDD', '1': 'DDD', '2': 'DDD',
                                '3': 'DDD', '4': 'DDD', '5': 'DDD', '6': 'DDD', 
                                '00': 'DDD', '01': 'STD', '02': 'DDD', '03': 'DDD', 
                                '04': 'DDD', '05': 'DDD', '06': 'DDD', 'S': 'STD', 
                                'B': 'SUB', 'D': 'DBT', 'M': 'SMA', 'L': 'LSS'}

    map_2 = {'XXX':0, 'DDD':0, 'STD':0, 'SMA':1, 'SUB':90, 'DBT':360, 'LSS':720}

    if type(data) == dict:
        date = dt.strptime(data['Year'] + data['Month'] + '01', '%Y%m%d')
        month = date.year*12 + date.month
        status = float(data['Days_Past_Due']) if data['Days_Past_Due'] != '' else 0
        #if data['Asset_Classification'] in ('00', '01', '02', '03', '04', '05', '06'):
        #    return None
        status_bucket = asset_classification_map[data['Asset_Classification']]
        status_bucket = map_2.get(status_bucket)
        res = np.column_stack((np.array(date), np.array(month), np.array(status),
                               np.array(status_bucket)))
    else:
        dates = [dt.strptime(i['Year'] + i['Month'] + '01', '%Y%m%d') for i in data]
        months = [date.year*12 + date.month for date in dates]
        statuses = [float(i['Days_Past_Due']) if i['Days_Past_Due'] != '' else 0 for i in data]
        #for i in data:
        #    if i['Asset_Classification'] in ('00', '01', '02', '03', '04', '05', '06'):
        #        return None
        status_buckets = [asset_classification_map[i['Asset_Classification']] for i in data]
        status_buckets = list(map(map_2.get, status_buckets))
        res = np.column_stack((np.array(dates), np.array(months), np.array(statuses),
                               np.array(status_buckets)))

    return res