import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# import from folders/theme changer
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

FONT_AWESOME = ["https://use.fontawesome.com/release/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_lacally=True
server=app.server

# ======== Layout ========== #

app.layout = dbc.Container(children=[

], fluid=True, style={'height':'100vh'})


# ======== Callbacks ======== #



# ====== Run Server ====== # 

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)