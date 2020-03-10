import pandas as pd
import numpy as np
from glob import glob
import os

REGIONI_DATA_PATH = 'COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv'

df = pd.read_csv(REGIONI_DATA_PATH, parse_dates=['data'])

fields = {
    'totale_casi': 'Casi totali',
    'totale_attualmente_positivi': 'Attualmente positivi',
    'isolamento_domiciliare': 'Isolamento domiciliare',
    'totale_ospedalizzati': 'Positivi ospedalizzati',
    'terapia_intensiva': 'Pazienti in terapia intensiva',
    'deceduti': 'Pazienti deceduti',
    'dimessi_guariti': 'Pazienti dimessi',
    'tamponi': 'Numero di tamponi',
}

regions = df['denominazione_regione'].unique()
regions = np.insert(regions, 0, 'Italia')

def get_regional_covid_data():
    global df
    dff = df.pivot(index='data',columns='denominazione_regione', values=fields.keys())
    sum_df = dff.sum(axis=1, level=0)
    sum_df.columns = pd.MultiIndex.from_product([sum_df.columns, ['Italia']])
    return pd.concat([dff,sum_df], axis=1).sort_index(axis=1)

if __name__ == '__main__':
    df = get_regional_covid_data()
    print(df.index)
