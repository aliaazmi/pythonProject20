import dash
import plotly.express as px
import plotly.io as pio
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash import Dash, html
import base64
from PIL import Image
from dash_table import DataTable
from app import app

df = pd.read_csv('https://raw.githubusercontent.com/aliaazmi/databreast/main/Raw_data_breast_cancer_2.csv')

df_filterd1 = df[df['STAGE'].isin(['I', 'II', 'III', 'IV'])]
fig1 = px.pie(df_filterd1, values='Count', names='STAGE',
              title='<b>Stage (n=893)</b>',
              labels='<b> STAGE </b>', color_discrete_sequence=px.colors.sequential.Purpor)
fig1.update_traces(textposition='inside', textinfo='percent+label+value', hole=.4, )
fig1.update_layout(
    annotations=[dict(text='<b>Stage<b>', x=0.5, y=0.5, font_size=16, showarrow=False),
                 ])

columns = [dict(id='Year', name='Year'),
           dict(id='year1', name='Amount of Pt', type='numeric'), ]

data = [
    dict(Year='2019', year1=519, ),
    dict(Year='2020', year1=596, ),
    dict(Year='2021', year1=538, ),
    dict(Year='2022-August', year1=391, ),
    dict(Year='Total', year1=2044, )]

dr_table = DataTable(columns=columns,
                     data=data,
                     sort_action='native',
                     derived_virtual_data=data,
                     style_table={'minHeight': '40vh',
                                  'height': '40vh',
                                  'overflowY': 'scrool'},
                     style_cell={"whitespace": 'normal',
                                 'height': 'auto',
                                 'fontFamily': 'verdana'},
                     style_header={'textAlign': 'center',
                                   'fontSize': 20},
                     style_data={'fontSize': 18},
                     style_data_conditional=[{'textAlign': 'center',
                                              'cursor': "pointer"},
                                             {'if': {'row_index': 'odd'}, 'backgroundColor': '#E6E6FA'}],

                     )

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=['<35', '36-55', '55>'],
    y=[91, 1013, 940],
    name='Female',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=2)
    )
))

fig3.update_layout(xaxis=dict(title_text='<b>Age</b>'),
                   margin=dict(t=5, b=85), )

labels = ['TNBC', 'HR-ve/HER2+ve', 'HR+ve/HER2+ve ',
          'HR+ve/HER2-ve ', ]
values = [173, 187, 303, 433]

fig7 = go.Figure(data=[go.Pie(labels=labels,values=values, textinfo='percent+label+value',
                              insidetextorientation='radial', textposition='inside',
                              marker_colors=px.colors.sequential.Burg)
                       ])

fig7.update_layout(
    title_text="<b>HR/HER2 (n=1096)</b>", showlegend=False,

)

pie1_graph = dcc.Graph(figure=fig7,
                       style={'gridArea': 'pie1'})
pie2_graph = dcc.Graph(figure=fig1,
                       style={'gridArea': 'pie2'})
bar_graph = dcc.Graph(figure=fig3,
                      style={'gridArea': 'bar'})
dr_table.style = {'gridArea': 'tables'}

container = html.Div([dr_table, bar_graph, pie1_graph, pie2_graph, ],
                     style={'display': 'grid',
                            'gridTemplateAreas': '"tables bar" "pie2 pie1"',
                            'gridTemplateColumns': '45vw 65vw',

                            'gridTemplateRows': '45vh 95vh',

                            'columnGap': '2px', })

title = html.H2("Beacon Hospital's Breast Cancer Statistic (2019-2022(August)",
                style={
                    'fontFamily': 'verdana',
                    'textAlign': 'center',
                },
                id='dashTitle',
                className="titles")

layout = html.Div([
    html.H2(title), html.H1(), html.Br(), html.Br(), html.Br(), html.Br(), container,
])


