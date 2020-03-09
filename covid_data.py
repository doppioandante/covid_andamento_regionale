import pandas as pd
from glob import glob
import os

REGIONI_DATA_PATH = 'COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv'

df = pd.read_csv(REGIONI_DATA_PATH, parse_dates=['data'])

fields = {
    'totale_attualmente_positivi': 'Totale attualmente positivi',
    'totale_ospedalizzati': 'Pazienti ospedalizzati',
    'terapia_intensiva': 'Pazienti in terapia intensiva',
    'deceduti': 'Pazienti deceduti',
    'dimessi_guariti': 'Pazienti dimessi',
}

regions = df['denominazione_regione'].unique()

def get_regional_covid_data():
    global df
    dff = df.pivot(index='data',columns='denominazione_regione', values=fields.keys())

    return dff

if __name__ == '__main__':
    df = get_regional_covid_data()
    print(df['totale_attualmente_positivi']['Abruzzo'])
