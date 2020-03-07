DATA_DIR = 'COVID-19/dati-regioni'

import pandas as pd
from glob import glob
import os

def get_regional_covid_data():
    dfs = []
    for csv_path in glob(os.path.join(DATA_DIR, '*.csv')):
        df = pd.read_csv(csv_path, parse_dates=['data'])
        interesting_fields = [
            'totale_attualmente_positivi',
            'denominazione_regione',
            'data'
        ]
        dfs.append(df.filter(items=interesting_fields))

    df = pd.concat(dfs)
    df = df.pivot(index='data',columns='denominazione_regione', values='totale_attualmente_positivi')
    return df

if __name__ == '__main__':
    df = get_regional_covid_data()
    print(df.columns)
