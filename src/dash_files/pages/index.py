import dash
from dash import dcc, html, callback

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Welcome to index!'),
])