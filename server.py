# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
from pathlib import Path
import dash
import dash_core_components as dcc
import dash_html_components as html

from covid_data import get_regional_covid_data

external_scripts = ["https://cdn.plot.ly/plotly-locale-it-latest.js"]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    url_base_pathname='/covid-19/'
)

covid_data = get_regional_covid_data()
last_update = ''
try:
    iso_timestamp = Path('update_timestamp.txt').read_text().strip()
    last_update = datetime.fromisoformat(iso_timestamp)
except:
    pass

app.title = 'Andamento territoriale contagi'
app.layout = html.Div(children=[
    html.H1(children='Andamento territoriale COVID-19'),

    html.Div([
        '''
        Visualizzazione degli andamenti territoriali del COVID-19.
        I dati sono aggiornati automaticamente dalla
        ''',
        html.A('fonte ufficiale della protezione civile', href='https://github.com/pcm-dpc/COVID-19'),
        '.', html.Br(),
        'Il codice è open source sotto licenza MIT e disponibile su ',
        html.A('github', href='https://github.com/doppioandante/covid_andamento_regionale'),
    ]),

    html.Div(f'''
        Ultimo aggiornamento: {last_update}
    '''),

    dcc.Graph(
        id='veneto-graph',
        figure={
            'data': [{
               'x': covid_data[nome_regione].index,
               'y': covid_data[nome_regione].to_list(),
               'name': nome_regione
            } for nome_regione in covid_data.columns],
            'layout': {
                'title': 'Totale attualmente positivi',
                'showlegend': True
            }
        },
        config=dict(
            locale='it'
        )
    )
])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run debug server')
    parser.add_argument('--port', dest='port', type=int, default=8080, help='HTTP server port')
    args = parser.parse_args()
    app.run_server(debug=True, port=args.port)
