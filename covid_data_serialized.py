import pickle

with open('serialized_time_series.pickle', 'rb') as f:
    serialized = pickle.load(f)

regions = serialized['regions']
extended_regions = serialized['extended_regions']
provinces = serialized['provinces']
fields = serialized['fields']
province_fields = serialized['province_fields']

def get_data_by_region():
    global serialized
    return serialized['by_region']

def get_data_by_province():
    global serialized
    return serialized['by_province']
