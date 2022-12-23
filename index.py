import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import home, colorectal_cancer, breast_cancer, lung_cancer

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home | ', href='/apps/home'),
        dcc.Link('Colorectal Cancer | ', href='/apps/colorectal_cancer'),
        dcc.Link('Breast Cancer | ', href='/apps/breast_cancer'),
        dcc.Link('Lung Cancer  ', href='/apps/lung_cancer'),
    ],
        className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home':
        return home.layout
    if pathname == '/apps/colorectal_cancer':
        return colorectal_cancer.layout
    if pathname == '/apps/breast_cancer':
        return breast_cancer.layout
    if pathname == '/apps/lung_cancer':
        return lung_cancer.layout
    else:
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=False)