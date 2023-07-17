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
        dbc.Col([ # Primeiro Card
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

        dbc.Col([ # Segundo Card
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Best Sellings Shops')
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=12),
                    ])
                    ])
                ]),
            ], style=tab_card),
        ], sm=8, lg=6),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph2', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=3)

    ], class_name='g-2 my-auto', style={'margin-top':'7px'}),
    
    # Row 2:
    dbc.Row([
        dbc.Col([ # Primeiro Card
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.Legend('Best Selling Products')
                    ]),
                    dbc.Row([
                        dcc.Graph(id='graph3', className='dbc', config=config_graph)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=6),

        dbc.Col([ # Segundo Card
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        html.Legend('Best Selling Product By Store')
                    ]),
                    dbc.Row([
                        dcc.Graph(id='graph4', className='dbc', config=config_graph)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                                dcc.Graph(id='Indicator2', className='dbc', config=config_graph)
                    ]),
                    dbc.Row([
                        dcc.Graph(id='Indicator3', className='dbc', config=config_graph)
                    ])
                ])
            ], style=tab_card),
        ], sm=12, lg=3)
    ], class_name='g-2 my-auto', style={'margin-top':'7px'})

], fluid=True, style={'height':'100vh'})


# ======== Callbacks ======== #

# ================= graph 1:
@app.callback(
    Output('graph1', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def graph1(toggle):
    template=template_theme1 if toggle else template_theme2

    Loja_Mais_Produtiva = dados_combinados_vendas.groupby('Loja').sum()
    Loja_Mais_Produtiva=Loja_Mais_Produtiva[['Quantidade Vendida']].sort_values(by='Quantidade Vendida', ascending=False)

    fig1 = px.bar(Loja_Mais_Produtiva, x=Loja_Mais_Produtiva.index, y='Quantidade Vendida',
                  hover_data=['Quantidade Vendida', Loja_Mais_Produtiva.index], color=Loja_Mais_Produtiva['Quantidade Vendida'],
                  labels={'Quantidade Vendida':'Quantidade Vendida'}, height=200)
    fig1.update_layout(main_config, template=template)
    fig1.update_layout({"margin": {"l":0, "r":0, "t":5, "b":0}})
    return fig1

# ================= graph 2:
@app.callback(
    Output('graph2', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph2(toggle):
    template=template_theme1 if toggle else template_theme2

    Loja_Mais_Produtiva = dados_combinados_vendas.groupby('Loja').sum()
    Loja_Mais_Produtiva=Loja_Mais_Produtiva[['Quantidade Vendida']].sort_values(by='Quantidade Vendida', ascending=False).reset_index()

    fig2 = go.Figure()
    fig2.add_trace(go.Indicator(
    mode='number+delta',
    title={"text": f"<span>{Loja_Mais_Produtiva['Loja'].iloc[0]} - Top Shop</span><br><span style='font-size:70%'>In sales in relation to the second shop</span><br>"},
    value=Loja_Mais_Produtiva['Quantidade Vendida'].iloc[0],
    delta={'relative': True, 'valueformat': '.1%', 'reference': Loja_Mais_Produtiva['Quantidade Vendida'].iloc[1]}
))
    fig2.update_layout(main_config, height=200, template=template)
    fig2.update_layout({"margin": {"l":40, "r":40, "t":70, "b":40}})
    return fig2


# ================= graph 3:
@app.callback(
    Output('graph3', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph3(toggle):
    template = template_theme1 if toggle else template_theme2

    Produtos_mais_vendidos=dados_combinados_vendas.groupby('Produto').sum()
    Produtos_mais_vendidos=Produtos_mais_vendidos[['Quantidade Vendida']].sort_values(by='Quantidade Vendida', ascending=False)
    Produtos_mais_vendidos

    fig3 = px.bar(Produtos_mais_vendidos, x=Produtos_mais_vendidos.index, y='Quantidade Vendida',
              hover_data=['Quantidade Vendida', Produtos_mais_vendidos.index], color='Quantidade Vendida',
              labels={'Quantidade Vendida':'Quantidade Vendida'}, height=200)
    fig3.update_layout(main_config, template=template)
    fig3.update_layout({"margin":{"l":0, "r":0, "t":5, "b":0}})
    return fig3


# ================= graph 4:

@app.callback(
    Output('graph4', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph4(toggle):
    template = template_theme1 if toggle else template_theme2

    Produto_mais_vendido_Loja = dados_combinados_vendas.groupby(['Loja', 'Produto'])['Quantidade Vendida'].sum()
    Produto_mais_vendido_Loja = Produto_mais_vendido_Loja.sort_values(ascending=False)
    Produto_mais_vendido_Loja = Produto_mais_vendido_Loja.groupby('Loja').head(1).reset_index()

    fig4 = go.Figure()
    fig4.add_trace(go.Pie(labels=Produto_mais_vendido_Loja['Loja']+'-'+Produto_mais_vendido_Loja['Produto'], values=Produto_mais_vendido_Loja['Quantidade Vendida'], hole=.5))
    fig4.update_layout(main_config, template=template, height=200, showlegend=False)
    fig4.update_layout({"margin":{"l":0, "r":0, "t":5, "b":0}})
    return fig4


@app.callback(
    Output('Indicator2', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def indicator2(toggle):
    template = template_theme1 if toggle else template_theme2

    dados_combinados_vendas['Faturamento']=dados_combinados_vendas['Quantidade Vendida'] * dados_combinados_vendas['Preco Unitario']
    dados_faturamento = dados_combinados_vendas.groupby('Produto').sum().reset_index()
    dados_faturamento = dados_faturamento[['Produto','Faturamento']].sort_values(by='Faturamento', ascending=False)

    fig5=go.Figure()
    fig5.add_trace(go.Indicator(
    mode='number+delta',
    title={"text": f"<span>{dados_faturamento['Produto'].iloc[0]} - Top Product</span><br><span style='font-size:70%'>Best Selling Product</span><br>"},
    value=dados_faturamento['Faturamento'].iloc[0],
    delta={'relative':True, 'valueformat':'.1%', 'reference':dados_faturamento['Faturamento'].iloc[1]}
    ))
    fig5.update_layout(main_config, template=template, height=150)
    fig5.update_layout({"margin": {"l":5, "r":5, "t":50, "b":5}})

    return fig5

@app.callback(
    Output('Indicator3', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def indicator(toggle):
    template=template_theme1 if toggle else template_theme2

    Vendedor_Mais_Vendeu = dados_combinados_vendas.groupby(['Primeiro Nome']).sum()
    Vendedor_Mais_Vendeu=Vendedor_Mais_Vendeu[['Preco Unitario']].sort_values(by='Preco Unitario', ascending=False).reset_index()

    fig6=go.Figure()
    fig6.add_trace(go.Indicator(
    mode='number+delta',
    title={"text": f"<span>{Vendedor_Mais_Vendeu['Primeiro Nome'].iloc[0]} - Top Seller</span><br><span style='font-size:70%'>Best Seller Among Stores </span><br>"},
    value=Vendedor_Mais_Vendeu['Preco Unitario'].iloc[0],
    delta={'relative':True, 'valueformat':'.1%', 'reference':Vendedor_Mais_Vendeu['Preco Unitario'].iloc[1]}
    ))

    fig6.update_layout(main_config, template=template, height=150)
    fig6.update_layout({"margin": {"l":5, "r":5, "t":70, "b":5}})

    return fig6
# ====== Run Server ====== # 

if __name__ == '__main__':
    app.run_server(debug=False, port=8051)