import pandas as pd
from glob import glob
import os

def get_regional_covid_data():
    DATA_PATH = 'COVID-19/dati-regioni/dpc-covid19-ita-regioni.csv'
    df = pd.read_csv(DATA_PATH, parse_dates=['data'])
    interesting_fields = [
        'totale_attualmente_positivi',
        'denominazione_regione',
        'data'
    ]
    df = df.filter(items=interesting_fields)
    df = df.pivot(index='data',columns='denominazione_regione', values='totale_attualmente_positivi')

    return df

if __name__ == '__main__':
    df = get_regional_covid_data()
    print(df)
