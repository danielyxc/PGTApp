import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas
from dash.dependencies import Input, Output
from app import app
from database.transforms import today, vessel_name, vessel_imo, start_date, end_date
from tabs import tab1, tab2
from database import transforms
import base64

df = transforms.df

PGT_marine_logo = 'PGMTLogo.jpg'
ENVI_marine_logo = 'ENVI EGCS Header.jpg'

layout = html.Div([
    html.Div([
        html.Div(
            html.Img(
                src=app.get_asset_url(PGT_marine_logo),
                style={
                    'height': '50px',
                    'width': '250px'}),
            className='one-third column'),
        html.Div(
            html.Img(
                src=app.get_asset_url(ENVI_marine_logo),
                style={
                    'height': '50px',
                    'width': '700px'}),
            className='two-thirds column'), ],
        style={
        'color': '#002332',
        'background': '#FFFFFF',
        'justify-content': 'space-between', },
        className='row flex-display'),
    html.Div([
        html.P('Vessel Name: ' + vessel_name,
               style={
                   'textAlign': 'center'},
               className='one-third column'),
        html.P('Vessel IMO: ' + vessel_imo,
               style={
                   'textAlign': 'center'},
               className='one-third column'),
        html.P('Printed On: ' + today,
               style={
                   'textAlign': 'center'},
               className='one-third column')],
             style={
        'background': '#FFFFFF'},
        className='row flex-display'),
    html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label='Data Analysis', value='tab-1'),
            dcc.Tab(label='Data Table', value='tab-2'), ]),
        html.Div(id='tabs-content')],
        style={
        'margin-top': '0px',
        'margin-bottom': '50px'})
])
