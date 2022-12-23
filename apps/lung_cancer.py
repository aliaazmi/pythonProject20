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
from app import app


df = pd.read_csv('https://raw.githubusercontent.com/aliaazmi/data_lung_cancer/main/Lung_cancer.csv')

columns = [dict(id='Year', name='Year'),
           dict(id='amount', name='Amount of Pt', type='numeric')]
data = [
    dict(Year='2019', amount=265),
    dict(Year='2020', amount=195),
    dict(Year='2021', amount=100),
    dict(Year='2022-August', amount=178),
    dict(Year='Total Pt', amount=738)]

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

df_filterd2 = df[df['Type_of_Lung_Cancer'].isin(['NSCLC', 'SCLC', 'Sarcoma',
                                                 'Malignant mesothelioma'])]
fig2 = px.pie(df_filterd2, values='Count', names='Type_of_Lung_Cancer',
              title='<b>Type of Lung Cancer (n=405)</b>',
              labels='Type_of_Lung_Cancer', color_discrete_sequence=px.colors.sequential.Purp)
fig2.update_traces(textposition='inside', textinfo='percent+label+value')

df_filterd1 = df[df['Stage'].isin(['I', 'II', 'III', 'IV'])]
fig1 = px.pie(df_filterd1, values='Count', names='Stage',
              title='<b>Stage for Lung Cancer Pt (n=380)</b>',
              labels='Stage', hole=.3, color_discrete_sequence=px.colors.sequential.Magenta)
fig1.update_traces(textposition='inside', textinfo='percent+label+value')

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=['<20', "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", '81>', ],
    y=[1, 7, 21, 63, 105, 152, 95, 24,],
    name='Female',
    marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=2)
    )
))
fig3.add_trace(go.Bar(
    x=['<20', "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", '81>', ],
    y=[0, 5, 19, 46, 104, 190, 135, 34, ],
    name='Male',
    marker=dict(
        color='rgba(58, 71, 80, 0.6)',
        line=dict(color='rgba(58, 71, 80, 1.0)', width=2)

    )
))
fig3.update_layout(xaxis=dict(title_text='<b>Age</b>'),
                   margin=dict(t=5, b=85))

title = html.H2("Beacon Hospital's Lung Cancer Statistic (2019-2022(August)",
                style={
                    'fontFamily': 'verdana',
                    'textAlign': 'center',
                },
                id='dashTitle',
                className="titles")

bar_graph = dcc.Graph(figure=fig3,
                      style={'gridArea': 'bar'})
pie1_graph = dcc.Graph(figure=fig2,
                       style={'gridArea': 'pie1'})
pie2_graph = dcc.Graph(figure=fig1,
                       style={'gridArea': 'pie2'})

dr_table.style = {'gridArea': 'tables'}

container = html.Div([dr_table, bar_graph, pie1_graph, pie2_graph],
                     style={'display': 'grid',
                            'gridTemplateAreas': '"tables bar" "pie2 pie1"',
                            'gridTemplateColumns': '45vw 55vw',

                            'gridTemplateRows': '45vh 95vh',
                           'columnGap': '2px', })

layout = html.Div([title, container])
