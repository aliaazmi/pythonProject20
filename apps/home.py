#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import plotly.express as px
import plotly.io as pio
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from dash.dependencies import Output, Input
import plotly.figure_factory as ff
import plotly.graph_objs as go
import dash_html_components as html
from dash_table import DataTable
import plotly.graph_objects as go
from plotly.graph_objs import Figure
from app import app

df = pd.read_csv('https://raw.githubusercontent.com/aliaazmi/data/main/Data_base_cancer_30.csv')



df_filterd2 = df[df['Year'].isin(['FEMALE', 'MALE'])]

fig = px.pie(df_filterd2, values='Count', names='Cancer',
             title='Beacon Hospital Cancer Pt Statistic 2019-2021',
             labels='Cancer', )
fig.update_traces(textposition='inside', textinfo='percent+label+value')

fig2 = px.pie(df, values='Count', names='Cancer',
              title="Cancer Pt Statistic (Overall)",
              labels='Cancer', color_discrete_sequence=px.colors.sequential.RdPu)
fig2.update_traces(textposition='inside', textinfo='percent+label+value')

df['Year'] = df['Year'].apply(str)

data = [
    dict(Year='2019', amount=1981),
    dict(Year='2020', amount=2367),
    dict(Year='2021', amount=2461),
    dict(Year='2022', amount=2232),
    dict (Year= '2023', amount= 929) 
  
]

columns = [
    dict(id='Year', name='Year'),
    dict(id='amount', name='Pt Amount', type='numeric'),
]
dr_table = DataTable(columns=columns,
                     data=data,
                     active_cell={'row': 0, 'column': 0},
                     sort_action='native',
                     derived_virtual_data=data,
                     style_table={'minHeight': '19vh',
                                  'height': '19vh',
                                  'overflowY': 'scrool'},
                     style_cell={"whitespace": 'normal',
                                 'height': 'auto',
                                 'fontFamily': 'verdana'},
                     style_header={'textAlign': 'center',
                                   'fontSize': 22},
                     style_data={'fontSize': 20},
                     style_data_conditional=[{'textAlign': 'center',
                                              'cursor': "pointer"},
                                             {'if': {'row_index': 'odd'}, 'backgroundColor': '#f2e5ff'}],

                     )

dr_table.style = {'gridArea': 'tables'}
pie1_graph = dcc.Graph(figure=fig, id="my-graph",
                       style={'gridArea': 'pie1'})

pie2_graph = dcc.Graph(figure=fig2,
                       style={'gridArea': 'pie2'})

container = html.Div([pie1_graph, pie2_graph, ],
                     style={'display': 'grid',
                            'gridTemplateAreas': '"pie1 pie2" ',
                            'gridTemplateColumns': '50vw 50vw',
                            'gridTemplateRows': '95vh', })

layout = html.Div([
    html.H1('Beacon Hospital Cancer Pt Statistic 2019-2023(May)'),
    dr_table, html.H1(""), html.H1(''),  html.Br(), html.Hr(), html.Br(), html.Br(),
    dcc.Dropdown(id='year-choice',
                 options=[{'label': x, 'value': x}
                          for x in sorted(df.Year.unique())],
                 value='2019', style={'width': '50%'}
                 ), html.Br(), html.Br(''), html.Br(''),
    container, html.Hr(),
])

@app.callback(
    Output(component_id="my-graph", component_property="figure"),
    Input(component_id="year-choice", component_property="value"),

)
def interactive_graphing(value_year):
    dff = df[df.Year == value_year]
    fig = px.pie(dff, values='Count', names='Cancer',
                 title='Cancer Pt Statistic by Year 2019-2023(May)',
                 labels='Cancer', color_discrete_sequence=px.colors.sequential.Agsunset)
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    return fig


