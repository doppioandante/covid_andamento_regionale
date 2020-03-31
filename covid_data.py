import pandas as pd
import numpy as np

REGIONI_DATA_PATH = 'COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv'
PROVINCE_DATA_PATH = 'COVID-19/dati-province/dpc-covid19-ita-province.csv'

df_regions = pd.read_csv(REGIONI_DATA_PATH, parse_dates=['data'])
df_provinces = pd.read_csv(PROVINCE_DATA_PATH, parse_dates=['data'])

fields = {
    'totale_casi': 'Casi totali',
    'totale_positivi': 'Attualmente positivi',
    'isolamento_domiciliare': 'Isolamento domiciliare',
    'totale_ospedalizzati': 'Positivi ospedalizzati',
    'terapia_intensiva': 'Pazienti in terapia intensiva',
    'deceduti': 'Pazienti deceduti',
    'dimessi_guariti': 'Pazienti dimessi',
    'tamponi': 'Numero di tamponi',
}

regions = df_regions['denominazione_regione'].unique()
extended_regions = np.insert(regions, 0, 'Italia')

# dict in the form {'Region': [list of provinces'])
dff = pd.DataFrame(df_provinces, columns=['denominazione_regione', 'denominazione_provincia'])
provinces = dff.drop_duplicates() \
    .groupby('denominazione_regione')['denominazione_provincia'] \
    .apply(list) \
    .to_dict()

province_fields = {
    'totale_casi': 'Casi totali'
}

def get_data_by_region():
    global df_regions
    dff = df_regions.pivot(index='data',columns='denominazione_regione', values=fields.keys())
    sum_df = dff.sum(axis=1, level=0)
    sum_df.columns = pd.MultiIndex.from_product([sum_df.columns, ['Italia']])
    return pd.concat([dff,sum_df], axis=1).sort_index(axis=1)

def get_data_by_province():
    global df_provinces
    dff = df_provinces.pivot_table(
        index='data',
        columns=['denominazione_regione', 'denominazione_provincia'],
        values=province_fields.keys()
    )
    return dff
