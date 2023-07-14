import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import os
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

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2=dbc.themes.DARKLY

# ======== Reading and cleaning File

def formata_valor(valor):
    return "R$ {:.2f}".format(valor)

dados_vendas = []
lista_arquivos = os.listdir(r'E:\Documentos-Victor\GitHub_Novo\Analise-De-Dados-E-Automacao-De-Processos\Projeto_Atualizado_01_Indicadores_de_vendas_e_devoluções\Vendas')

for arquivos in lista_arquivos:
    if "Vendas" in arquivos:
        dados_doc = pd.read_csv(fr'E:\Documentos-Victor\GitHub_Novo\Analise-De-Dados-E-Automacao-De-Processos\Projeto_Atualizado_01_Indicadores_de_vendas_e_devoluções\Vendas\{arquivos}')
        dados_vendas.append(dados_doc)
        
dados_combinados_vendas=pd.concat(dados_vendas)
dados_combinados_vendas.to_csv('dados_combinados.csv', index=False)

# ======== Layout ========== #

app.layout = dbc.Container(children=[
# Row 1:
    dbc.Row([ # Linha 1 da tela
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Sales Analytics")
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-balance-scale', style={'font-size':'300%'})
                        ], sm=4, align='center'),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("VS Analytics")
                        ])
                    ], style={"margin-top":'10px'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Visit our GitHub: ", href="https://github.com/VictorSayoan", target="blank")
                        ], style={"margin-top":'10px'}, align='center')
                    ])

                ]),
            ], style=tab_card),
        ], sm=4, lg=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Best Sellings Products')
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=12),
                    ])
                    ])
                ]),
            ], style=tab_card),
        ], sm=12, lg=6),

    ], class_name='g-2 my-auto', style={'margin-top':'7px'})

], fluid=True, style={'height':'100vh'})


# ======== Callbacks ======== #

#graph 1:
@app.callback(
    Output('graph1', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def graph1(toggle):
    template=template_theme1 if toggle else template_theme2

    Loja_Mais_Produtiva = dados_combinados_vendas.groupby('Loja').sum()
    Loja_Mais_Produtiva=Loja_Mais_Produtiva[['Quantidade Vendida']].sort_values(by='Quantidade Vendida', ascending=False)

    fig1 = px.bar(Loja_Mais_Produtiva, x=Loja_Mais_Produtiva.index, y='Quantidade Vendida',
                  hover_data=['Quantidade Vendida', Loja_Mais_Produtiva.index], color='Quantidade Vendida',
                  labels={'Quantidade Vendida':'Quantidade Vendida'}, height=200)
    fig1.update_layout(main_config, template=template)
    
    return fig1


# ====== Run Server ====== # 

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)