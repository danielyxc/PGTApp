import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly
from app import app
from dash.dependencies import Input, Output
from tabs import header, tab1, tab2
from database import transforms

app.layout = header.layout


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.layout
    elif tab == 'tab-2':
        return tab2.layout


if __name__ == '__main__':
    app.run_server(debug=True)
