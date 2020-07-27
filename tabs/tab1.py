import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from dash.dependencies import Input, Output
from app import app
from database import transforms
import datetime as dt
import plotly.graph_objs as go
import plotly.express as px
from database import transforms
from database.transforms import today, vessel_name, vessel_imo, start_date, end_date
import statsmodels


df = transforms.df

controls = dbc.Container(
    dbc.Card([
        html.H3('Filters',
                style={
                    'textAlign': 'center',
                    'border-bottom': '2px solid rgba(196, 196, 196, 0.5)'}),
        dbc.FormGroup([
            dbc.Label("Averages",
                      style={
                          'textAlign': 'center',
                          'font-weight': 'bold'}),
            dcc.RadioItems(
                id='rolling-average',
                options=[
                    {'label': ' Hourly Average', 'value': 'H'},
                    {'label': ' Daily Average', 'value': 'D'},
                    {'label': ' 2-minute Data', 'value': 'null'},
                    {'label': ' 15 minute Rolling Average(TBD)',
                     'value': 'TBD'}])]),
        dbc.FormGroup([
            dbc.Label("Date Range Selector",
                      style={
                          'textAlign': 'center',
                          'font-weight': 'bold'}),
            dcc.DatePickerRange(
                id='date-range-selector',
                min_date_allowed=start_date,
                max_date_allowed=end_date,
                start_date=df.Date.min(),
                end_date=df.Date.max())],
            style={'margin-top': '30px'}),
        dbc.FormGroup([
            dbc.Label("Parameter Selector",
                      style={
                          'textAlign': 'center',
                          'font-weight': 'bold'}),
            dcc.Dropdown(
                id='parameters-dropdown',
                options=[{'label': i, 'value': i}
                         for i in df.columns],
                placeholder=' Select figure parameters',
                value='FT201',
                multi=True)],
            style={'margin-top': '30px'})]))

regressioncontrols = dbc.FormGroup([
    html.Div([
        dbc.Label("X-Variable",
                  style={
                      'textAlign': 'center',
                      'font-weight': 'bold'}),
        dcc.Dropdown(
            id='x-label-dropdown',
            options=[{'label': i, 'value': i}
                     for i in df.columns],
            value='SO2')],
        className='six columns'),
    html.Div([
        dbc.Label("Y-Variable",
                  style={
                      'textAlign': 'center',
                      'font-weight': 'bold'}),
        dcc.Dropdown(
            id='y-label-dropdown',
            options=[{'label': i, 'value': i}
                     for i in df.columns],
            value='ME_Load')],
        className='six columns')])

multicontrols = html.Div([
    dbc.Label("Parameters",
              style={
                  'textAlign': 'center',
                  'font-weight': 'bold'}),
    dcc.Dropdown(
        id='multi-param-selector',
        options=[{'label': i, 'value': i}
                 for i in ['Flows', 'Temperatures (°C)', 'Gas Pressures (kPa)', 'Water Pressures (MPa)', 'CEMS', 'WWMS']],
        value='Flows')],
    className='twelve columns')

layout = html.Div([
    html.Div([
        html.Div(controls,
                 className='pretty_container four columns'),
        html.Div(id='time-series-plot',
                 className='pretty_container eight columns')],
             style={'justify-content': 'space-between'},
             className='row flex-display'),
    html.Div([
        html.Div([
            html.Div(regressioncontrols,
                     className=' tweleve columns'),
            html.Div(id='regression-plot',
                     className='tweleve columns',
                     style={'margin-left': '0px'})],
                 className="pretty_container six columns"),
        html.Div([
            html.Div(multicontrols,
                     className='twelve columns'),
            html.Div(
                id='multi-param-plot',
                className='twelve columns')],
            className='pretty_container six columns')],
        className='row flex-display',
        style={
        'justify-content': 'space-between'})],
    id='maincontainer',
    style={
        'display': 'flex',
        'flex-direction': 'column'})


@app.callback(Output('time-series-plot', 'children'),
              [Input('date-range-selector', 'start_date'),
               Input('date-range-selector', 'end_date'),
               Input('parameters-dropdown', 'value'),
               Input('rolling-average', 'value')])
def update_timeseries(start_date, end_date, parameters, rolling_average):
    if rolling_average == 'H':
        filtered_df = df.resample('H').mean()
    elif rolling_average == 'D':
        filtered_df = df.resample('D').mean(),
    elif rolling_average == 'TBD':
        filtered_df = df
        filtered_df['TBD101_inlet'] = filtered_df['TBD101_inlet'].rolling(
            7).mean()
        filtered_df['TBD101_outlet'] = filtered_df['TBD101_outlet'].rolling(
            7).mean()
        filtered_df['TBD101_difference'] = filtered_df['TBD101_difference'].rolling(
            7).mean()
    else:
        filtered_df = df

    start_date_obj = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = dt.datetime.strptime(end_date, '%Y-%m-%d')
    filtered_df = filtered_df[start_date_obj: end_date_obj]

    fig = go.Figure()
    if isinstance(parameters, str):
        fig.add_trace(go.Scatter(x=filtered_df.index,
                                 y=filtered_df[parameters], name=parameters))
    else:
        for parameter in parameters:
            fig.add_trace(go.Scatter(x=filtered_df.index,
                                     y=filtered_df[parameter], name=parameter))

    return html.Div([
                    dcc.Graph(
                        id='time-series',
                        figure=fig)
                    ])


@app.callback(Output('regression-plot', 'children'),
              [Input('date-range-selector', 'start_date'),
               Input('date-range-selector', 'end_date'),
               Input('x-label-dropdown', 'value'),
               Input('y-label-dropdown', 'value')])
def update_regression(start_date, end_date, x_label, y_label):
    filtered_df = df
    start_date_obj = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = dt.datetime.strptime(end_date, '%Y-%m-%d')
    filtered_df = filtered_df[start_date_obj: end_date_obj]
    fig = px.scatter(
        x=filtered_df[x_label],
        y=filtered_df[y_label],
        labels={
            'x': x_label,
            'y': y_label},
        trendline='ols')
    return html.Div(
        dcc.Graph(figure=fig))


@app.callback(Output('multi-param-plot', 'children'),
              [Input('date-range-selector', 'start_date'),
               Input('date-range-selector', 'end_date'),
               Input('multi-param-selector', 'value')])
def multi(start_date, end_date, parameters):
    filtered_df = df
    start_date_obj = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = dt.datetime.strptime(end_date, '%Y-%m-%d')
    filtered_df = filtered_df[start_date_obj: end_date_obj]
    trace1 = go.Figure()
    if parameters == 'Flows':
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['FT201'], name='FT201'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['FT202'], name='FT202'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['FT203'], name='FT203'))

    elif parameters == 'Temperatures (°C)':
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['TT201'], name='TT201'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['TT202'], name='TT202'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['TT203'], name='TT203'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['TT204'], name='TT204'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['TT205'], name='TT205'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['TT206'], name='TT206'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['TT208'], name='TT208'))
    elif parameters == 'Gas Pressures (kPa)':
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT205'], name='PT205'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT206'], name='PT206'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT207'], name='PT207'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT208'], name='PT208'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT209'], name='PT209'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT211'], name='PT211'))
    elif parameters == 'Water Pressures (MPa)':
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT201'], name='PT201'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT202'], name='PT202'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['PT203'], name='PT203'))
    elif parameters == 'CEMS':
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['SO2'], name='SO2'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['CO2'], name='CO2'))
        trace1.add_trace(go.Scatter(x=filtered_df.index,
                                    y=filtered_df['SO2CO2'], name='SO2CO2'))
    # elif parameters == 'WWMS':

    return dcc.Graph(
        id='multi-param',
        figure=trace1
    )
