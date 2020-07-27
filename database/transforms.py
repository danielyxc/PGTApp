import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime


now = datetime.now()
today = now.strftime('%d/%m/%Y %H:%M:%S')
df = pd.read_csv(
    '/Users/artemsoroka/Desktop/DashApp/Version_1/database/DataLogger1.csv')
df['datetime'] = pd.to_datetime(df['Time'])
df = df.set_index('datetime')
new = df['Time'].str.split(' ', n=1, expand=True)
df['Date'] = new[0]
df['Time'] = new[1]
end_date = df.index.max()
start_date = df.index.min()
vessel_name = str(df.Vessel_Name[-1])
vessel_imo = str(int(df.IMO_NO[-1]))
table_df = df
table_df = table_df.round({'ME_Load': 1, 'SO2': 1, 'CO2': 1, 'SO2CO2': 1,
                           'PH102': 1, 'PAH101_difference': 1, 'TBD101_difference': 1})
