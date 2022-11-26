from dash import html, dcc, Dash
from config import settings

app = Dash(__name__)

app.layout = html.Div([
    html.H1('hello world'),
    html.P(f'this is a={settings.a}!'),
])

if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port)