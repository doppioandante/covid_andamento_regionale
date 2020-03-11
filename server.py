# -*- coding: utf-8 -*-
import argparse
from datetime import datetime
from pathlib import Path
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import covid_data_serialized as covid_data

external_scripts = ["https://cdn.plot.ly/plotly-locale-it-latest.js"]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    url_base_pathname='/covid-19/'
)

by_region = covid_data.get_data_by_region()
by_province = covid_data.get_data_by_province()
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
        '.'
    ]),

    html.Div(f'''
        Ultimo aggiornamento: {last_update}
    '''),

    dcc.RadioItems(
        id='plot-type',
        options=[{'label': i, 'value': i} for i in ['Confronto Regioni', 'Dettaglio Regione', 'Dettaglio Province per Regione']],
        value='Confronto Regioni',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Dropdown(
        id='plot-variable'
    ),
    dcc.Graph(
        id='trend-plot',
        config=dict(
            locale='it'
        )
    )
])

@app.callback(
    Output('plot-variable', 'options'),
    [Input('plot-type', 'value')])
def set_dropdown_options(plot_type):
    if plot_type == 'Confronto Regioni':
        return [{'label': label, 'value': key} for key, label in covid_data.fields.items()]
    elif plot_type == 'Dettaglio Regione':
        return [{'label': r, 'value': r} for r in covid_data.extended_regions]
    elif plot_type == 'Dettaglio Province per Regione':
        return [{'label': r, 'value': r} for r in covid_data.regions]

@app.callback(
    Output('plot-variable', 'value'),
    [Input('plot-variable', 'options')])
def set_plot_variable(available_options):
    return available_options[0]['value']

@app.callback(
    Output('trend-plot', 'figure'),
    [Input('plot-type', 'value'),
     Input('plot-variable', 'value')]
)
def update_graph(plot_type, plot_variable):
    if plot_type == 'Confronto Regioni':
        return {
            'data': [{
               'x': by_region[plot_variable][nome_regione].index,
               'y': by_region[plot_variable][nome_regione].to_list(),
               'name': nome_regione,
               'visible': 'legendonly' if nome_regione == 'Italia' else 'true'
            } for nome_regione in covid_data.extended_regions],
            'layout': {
                'title': covid_data.fields[plot_variable],
                'showlegend': True
            }
        }
    elif plot_type == 'Dettaglio Regione':
        region = plot_variable
        return {
            'data': [{
               'x': by_region[key][region].index,
               'y': by_region[key][region].to_list(),
               'name': covid_data.fields[key],
               'visible': 'legendonly' if key == 'tamponi' else 'true'
            } for key in covid_data.fields.keys()],
            'layout': {
                'title': 'Trend ' + region,
                'showlegend': True
            }
        }
    elif plot_type == 'Dettaglio Province per Regione':
        region = plot_variable
        key = list(covid_data.province_fields.keys())[0]
        return {
            'data': [{
               'x': by_province[key][region][province_name].index,
               'y': by_province[key][region][province_name].to_list(),
               'name': province_name
            } for province_name in covid_data.provinces[region]],
            'layout': {
                'title': 'Casi totali - ' + region,
                'showlegend': True
            }
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run debug server')
    parser.add_argument('--port', dest='port', type=int, default=8080, help='HTTP server port')
    args = parser.parse_args()
    app.run_server(debug=True, port=args.port)
