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
from dash import Dash, html
import base64
from PIL import Image
from dash_table import DataTable
from app import app

df = pd.read_csv('https://raw.githubusercontent.com/aliaazmi/colorectal_site/main/Database_Colorectal_cancer3.csv')

# Using direct image file pathhttps://raw.githubusercontent.com/aliaazmi/data_lung_cancer/main/Lung_cancer.csv
image_path = 'assets/my-image2.jpeg'

# Using Pillow to read the image
pil_img = Image.open('assets/my-image2.jpeg')


# Using base64 encoding and decoding
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/jpeg;base64,' + base64.b64encode(image).decode('utf-8')


title = html.H2("Beacon Hospital's Colorectal Cancer Statistic (2019-2022(July)",
                style={
                    'fontFamily': 'verdana',
                    'textAlign': 'center',
                },
                id='dashTitle',
                className="titles")
columns = [dict(id='Year', name='Year'),
           dict(id='amount', name='Amount of Pt', type='numeric')]
data = [
    dict(Year='2019', amount=260),
    dict(Year='2020', amount=198),
    dict(Year='2021', amount=326),
    dict(Year='2022-July', amount=120),
    dict(Year='Total Pt', amount=904)]
dr_table = DataTable(columns=columns,
                     data=data,
                     sort_action='native',
                     derived_virtual_data=data,
                     style_table={'minHeight': '70vh',
                                  'height': '70vh',
                                  'overflowY': 'scrool'},
                     style_cell={"whitespace": 'normal',
                                 'height': 'auto',
                                 'fontFamily': 'verdana'},
                     style_header={'textAlign': 'center',
                                   'fontSize': 26},
                     style_data={'fontSize': 24},
                     style_data_conditional=[{'textAlign': 'center',
                                              'cursor': "pointer"},
                                             {'if': {'row_index': 'odd'}, 'backgroundColor': '#FF9912'}],

                     )
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=['<35', '36-50', '51-65', '65>', ],
    y=[13, 76, 150, 158, ],
    name='Female',
    marker=dict(
        color='RGB(255,127,36.0.3)',
        line=dict(color='RGB(23,23,23)', width=2)
    )
))
fig3.add_trace(go.Bar(
    x=['<35', '36-50', '51-65', '65>', ],
    y=[6, 79, 205, 212, ],
    name='Male',
    marker=dict(
        color='RGB(39,64,139, 0.3)',
        line=dict(color='RGB(23,23,23)', width=2)

    )
))
fig3.update_layout(xaxis=dict(title_text='<b>Age</b>'),
                   margin=dict(t=5, b=85))

df_filterd1 = df[df['Stage_AJC'].isin(['I', 'II', 'III', 'IV'])]
fig1 = px.pie(df_filterd1, values='Count', names='Stage_AJC',
              title='<b>Stage for Colorectal Cancer Pt (n=436)</b>',
              labels='Stage_AJC', hole=.3, color_discrete_sequence=px.colors.sequential.Turbo)
fig1.update_traces(textposition='inside', textinfo='percent+label+value')

pie1_graph = dcc.Graph(figure=fig1,
                       style={'gridArea': 'pie1'})

bar_graph = dcc.Graph(figure=fig3,
                      style={'gridArea': 'bar'})


container = html.Div([bar_graph, pie1_graph,],
                     style={'display': 'grid',
                             'gridTemplateAreas': '"pie1 bar"',
                            'gridTemplateColumns': '50vw 50vw',

                            'gridTemplateRows': '95vh',
                             'columnGap': '2px', })


layout = html.Div([
    html.H2(title), html.Img(src=pil_img), html.Br(), html.Hr(), html.Br(), html.Br(), html.Br(),
    html.Br(),  html.Br(), html.Br(),  html.Br(), html.Br(),  html.Br(),
    dr_table, html.Br(),  html.Br(), html.Br(),  html.Br(),
    container,
])

