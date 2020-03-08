# -*- coding: utf-8 -*-
import argparse
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

app.title = 'Andamento regionali contagi'
app.layout = html.Div(children=[
    html.H1(children='Andamento regionale COVID-19'),

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
