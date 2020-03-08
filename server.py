# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from covid_data import get_regional_covid_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

covid_data = get_regional_covid_data()

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
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
