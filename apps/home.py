import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Read the data from the CSV file
url = 'https://raw.githubusercontent.com/aliaazmi/data/main/Data_base_cancer_31.csv'
df = pd.read_csv(url, encoding='ISO-8859-1')

# Get yearly counts
yearly_counts = df.groupby('Year')['Count'].sum().reset_index()

# Get overall counts for each cancer
cancer_counts = df.groupby('Cancer')['Count'].sum().reset_index()

# Define the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define custom colors for the pie chart
pie_chart_colors = ['#FFCDD2', '#B39DDB', '#80DEEA', '#FFAB91', '#9FA8DA', '#A5D6A7']

# Define custom colors for the bar chart
bar_chart_colors = ['#FF7043', '#5C6BC0', '#26A69A', '#D81B60', '#7986CB', '#66BB6A']

# Define the layout for the app
app.layout = html.Div([
    html.H1('Beacon Hospital Cancer Pt Statistic 2019-2023 (until May)', className="mt-4 mb-5 text-center"),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='year-choice-bar',
                options=[{'label': x, 'value': x} for x in sorted(df.Year.unique())],
                value='2019',
                style={'width': '100%'}
            ),
            dcc.Graph(
                id='cancer-year-bar-chart',
                style={'height': '495px'}
            )
        ], width=6),  # Specify that this column takes 6 out of 12 columns (i.e., half of the row)
        dbc.Col([
            dcc.Graph(
                id='overall-pie-chart',
                style={'height': '485px'}
            )
        ], width=6)  # Specify that this column takes 6 out of 12 columns (i.e., half of the row)
    ]),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='yearly-table',
                columns=[
                    {"name": "Year", "id": "Year"},
                    {"name": "Cases Count", "id": "Count"}
                ],
                data=yearly_counts.to_dict('records'),
                style_table={'height': '400px', 'overflowY': 'auto'},
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'fontFamily': 'verdana',
                    'textAlign': 'center',  # Center align text in cells
                    'padding': '6px'  # Add padding to the cells
                },
                style_header={
                    'backgroundColor': '#f2f2f2',  # Set header background color
                    'fontWeight': 'bold',  # Bold font for header cells
                },
                style_data={'fontSize': 14},  # Reduce font size for data cells
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f9f9f9'  # Alternate row background color
                    },
                    {
                        'if': {
                            'filter_query': '{Count} > 1000',
                            'column_id': 'Count'
                        },
                        'backgroundColor': '#f0fafd',  # Light blue background for counts > 1000
                        'color': 'black'  # Font color for counts > 1000
                    },
                    {
                        'if': {
                            'filter_query': '{Count} <= 1000',
                            'column_id': 'Count'
                        },
                        'backgroundColor': '#ffe6e6',  # Light red background for counts <= 1000
                        'color': 'black'  # Font color for counts <= 1000
                    }
                ],
            )
        ], width=12)
    ]),
    
    html.Br(),
    
    html.H2('Insights'),
    html.P('The Beacon Hospital Cancer Pt Statistic dashboard provides an overview of cancer cases '
           'from the year 2019 to 2023. It allows users to explore the distribution of cancer cases '
           'by year and cancer type in the bar chart on the left. The pie chart on the right displays the overall '
           'cancer statistics for different types of cancer.'),
    html.P('Users can select a specific year from the bar chart dropdown to view the cancer distribution for '
           'that particular year. The table below shows the amount of cancer cases for each year. Users can click on the '
           'table headers to sort the data by year or cases count.'),
    
    dcc.Link('Go back to home', href='/'),
])

@app.callback(
    Output('cancer-year-bar-chart', 'figure'),
    Input('year-choice-bar', 'value')
)
def update_cancer_year_bar_chart(selected_year):
    dff = df[df['Year'] == int(selected_year)]
    dff_sum = dff.groupby('Cancer')['Count'].sum().reset_index()
    dff_sum = dff_sum.sort_values('Count', ascending=False)  # Sort the data in descending order
    fig_cancer_year_bar = px.bar(
        dff_sum, x='Cancer', y='Count', color='Cancer', title=f'Cancer Pt Statistic in {selected_year}',
        labels={'Cancer': 'Cancer Type', 'Count': 'Cases Count'}, text='Count',
        color_discrete_sequence=bar_chart_colors,  # Use custom colors for the bar chart
        category_orders={'Cancer': dff_sum['Cancer']}  # Maintain the order of the x-axis labels
    )
    fig_cancer_year_bar.update_traces(
        texttemplate='%{text}', textposition='outside',
        marker=dict(line=dict(width=1, color='DarkSlateGrey')), opacity=0.8  # Add border to the bars
    )
    fig_cancer_year_bar.update_layout(
        xaxis=dict(title=''),  # Empty string to remove the x-axis title
        yaxis=dict(title=''),  # Empty string to remove the y-axis title
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        font=dict(size=16, color="#4c4c4c"),
        margin=dict(l=60, r=20, t=60, b=40),
        hovermode="x",
        hoverlabel=dict(bgcolor="#f9f9f9", font_size=16, font_family="Arial"),
        showlegend=False  # Hide the legend
    )
    return fig_cancer_year_bar

@app.callback(
    Output('overall-pie-chart', 'figure'),
    Input('year-choice-bar', 'value')
)
def update_overall_pie_chart(selected_year):
    dff_sum = df.groupby('Cancer')['Count'].sum().reset_index()
    fig_overall_pie = px.pie(
        dff_sum, values='Count', names='Cancer', title='Overall Cancer Pt Statistic',
        color_discrete_sequence=pie_chart_colors,  # Use custom colors for the pie chart
        labels={'Cancer': 'Cancer Type'}
    )
    fig_overall_pie.update_traces(
        textposition='inside',
        textinfo='percent+label+value',
        insidetextfont=dict(size=14),
        marker=dict(line=dict(width=1, color='DarkSlateGrey')),
        opacity=0.8
    )
    fig_overall_pie.update_layout(
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        font=dict(size=16, color="#4c4c4c"),
        margin=dict(l=20, r=20, t=60, b=40),
        hovermode="closest",
        hoverlabel=dict(bgcolor="#f9f9f9", font_size=16, font_family="Arial"),
        showlegend=False  # Hide the legend
    )
    return fig_overall_pie

