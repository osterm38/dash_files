import dash
from dash import html, dcc, Dash
from config import settings

app = Dash(
    __name__,
    use_pages=True,    
)

app.layout = html.Div([
    html.H1('hello world'),
    html.P(f'this is a sentence'),
    dash.page_container,
])

if __name__ == "__main__":
    # TODO: add gunicorn here, or figure out how to use gunicorn from cli with settings?
    app.run(
        host=settings.host,
        port=settings.port,
        debug=True,
    )