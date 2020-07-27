import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Row(
    [
        dbc.Col(html.P('ENVI-Marine Exhaust Gas Cleaning System'), width=12,
                style={'justify-content': 'end'})
    ]
)
if __name__ == '__main__':
    app.run_server(debug=True)
