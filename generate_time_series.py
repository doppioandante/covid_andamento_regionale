import pickle
import covid_data

if __name__ == '__main__':
    to_serialize = dict(
      regions=covid_data.regions,
      extended_regions=covid_data.extended_regions,
      provinces=covid_data.provinces,
      fields=covid_data.fields,
      province_fields=covid_data.province_fields,
      by_region=covid_data.get_data_by_region(),
      by_province=covid_data.get_data_by_province(),
    )
    with open('serialized_time_series.pickle', 'wb') as f:
        pickle.dump(to_serialize, f)


