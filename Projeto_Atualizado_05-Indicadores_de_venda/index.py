import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# import from folders/theme changer
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[FONT_AWESOME, dbc.themes.QUARTZ])
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_lacally=True
server=app.server


# ======== Styles ========== #

tab_card = {'height': '100%'}
main_config={
    "hovermode":"x unified",
    "legend":{"yanchor":"top", 
             "y":0.9,
             "xanchor":"left",
             "x":0.1,
             "title":{"text":None},
             "font":{"color":"white"},
             "bgcolor":"rgba(0,0,0,0.5)"},
    "margin":{"l":10, "r":10, "t":10, "b":10}
    }

config_graph = {"displayModeBar":False, "showTips":False}

# ======== Reading and cleaning File

Dataset = pd.read_excel(r"E:\Documentos-Victor\Arquivos_GitHub\Analise-De-Dados-E-Automacao-De-Processos\Projeto_Atualizado_05-Indicadores_de_venda\Vendas.xlsx")

Database_Atualizado=Dataset.copy()
Database_Atualizado.drop('Data', axis=1, inplace=True)

df_1=Database_Atualizado.groupby(['ID Loja'])['Quantidade'].sum().reset_index()
df_1=df_1.sort_values(by='Quantidade', ascending=False)

# ======== Layout ========== #
    # Primeira Linha:
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([ # Primeiro Card
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Sales Analytics", style={'text-align': 'center'}),
                            html.Legend("Vs Analytics", style={'text-align': 'center'})
                        ], sm=8),
                        dbc.Col([
                            html.Div(
                                html.I(className='fa fa-balance-scale', style={'font-size': '300%'}),
                            )
                        ], sm=4, align='center'),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div(
                                dbc.Button("Visit our GitHub: ", href="https://github.com/VictorSayoan", target="blank",
                                           style={'font-family': 'Roboto', 'font-size': '18px'}),
                                className="d-flex justify-content-center"
                            )
                        ], style={"margin-top": '10px'}, align='center')
                    ])
                ]),
            ], style=tab_card),
        ], sm=4, lg=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dcc.Graph(
                                    id='graph1',
                                    figure=px.bar(df_1, x=df_1.index, y='Quantidade', labels={'Quantidade': 'Quantidade'},
                                                  height=200).update_layout(template=dbc.themes.QUARTZ)
                                    )
                            ], style=tab_card)
                        ], style={"margin-top": '10px'}, align='center')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dcc.Graph(id='graph2', className='dbc', config=config_graph)
                            ], style=tab_card)
                        ], style={"margin-top": '10px'}, align='center')
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=5)
    ], class_name='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, style={'height': '100vh'})

# ======== Callbacks ======== #



# ====== Run Server ====== # 

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)