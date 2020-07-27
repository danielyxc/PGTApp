import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
from app import app
from database import transforms
import datetime as dt
from database import transforms
from database.transforms import today, vessel_name, vessel_imo, start_date, end_date

df = transforms.table_df
controls = dbc.FormGroup([
    dbc.Label("Date Range Selector",
              style={
                  'textAlign': 'center',
                  'font-weight': 'bold'
              }),
    dcc.DatePickerRange(
        id='date-range-selector',
        min_date_allowed=start_date,
        max_date_allowed=end_date,
        start_date=df.Date.min(),
        end_date=df.Date.max())],
    style={'margin-top': '30px'})

layout = html.Div([
    html.Div(controls,
             className='pretty_container twelve columns'),
    html.Div(
        id='data-table',
        className='pretty_container twelve columns')],
    style={
        'justify-content': 'space-between'},
    className='row flex-display')


@app.callback(Output('data-table', 'children'),
              [Input('date-range-selector', 'start_date'),
               Input('date-range-selector', 'end_date')])
def update_graph(start_date, end_date):
    filtered_df = df
    start_date_obj = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = dt.datetime.strptime(end_date, '%Y-%m-%d')
    filtered_df = filtered_df[start_date_obj: end_date_obj]

    return html.Div(dash_table.DataTable(
        id='returned-table',
        columns=[
            {'name': i, 'id': i, 'deletable': True} for i in filtered_df[
                ['Date', 'Time', 'LA', 'LO', 'ME_Load', 'SO2', 'CO2', 'SO2CO2',
                 'PH102', 'PAH101_difference', 'TBD101_difference']]],
        data=filtered_df.to_dict('records'),
        style_cell={
            'textAlign': 'center'},
        style_header={
            'fontWeight': 'bold',
            'backgroundColor': 'rgb(230, 230, 230)'},
        style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'}]))
