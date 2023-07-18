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

Lista_Dados=[]
Lista_arquivos = os.listdir(r"E:\Documentos-Victor\GitHub_Novo\Analise-De-Dados-E-Automacao-De-Processos\Projeto_Atualizado_01_Indicadores_de_vendas_e_devoluções\Vendas")

for arquivo in Lista_arquivos:
    if "Devolucoes" in arquivo:
        Arquivos_Importantes=pd.read_csv(f'E:\Documentos-Victor\GitHub_Novo\Analise-De-Dados-E-Automacao-De-Processos\Projeto_Atualizado_01_Indicadores_de_vendas_e_devoluções\Vendas\{arquivo}')
        Lista_Dados.append(Arquivos_Importantes)

Lista_Arquivos_Concatenados=pd.concat(Lista_Dados)
Lista_Arquivos_Concatenados.to_csv('Lista_Arquivos_Concatenados.csv', index=False)

# ======== Layout ======= #
app.layout = dbc.Container(children=[

#Row 1:
    dbc.Row([
        dbc.Col([ # Primeiro Card
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([html.Legend('Returns Analytics')]),
                        dbc.Col([html.I(className='fa fa-balance-scale', style={'font-size':'300%'})], sm=4, align='center')
                    ]),
                    dbc.Row([
                        dbc.Col([ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]), html.Legend("VS Analytics")], style={"margin-top":'10px'})
                    ]),
                    dbc.Row([
                        dbc.Col([dbc.Button("Visit our GitHub: ", href="https://github.com/VictorSayoan", target="blank")], style={"margin-top":'10px'}, align='center')
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=3),

        dbc.Col([ # Segundo Card
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H4('Stores With More Returns'),
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                            ]),
                        dbc.Col([
                            html.H4('Most returned Products in All Stores'),
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                            ])
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=9)
    ], class_name='g-2 my-auto', style={'margin-top':'7px'}),

# Row 2:
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Most Returned Product by Store'),
                    dcc.Graph(id='graph3', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Value of returns'),
                    dcc.Graph(id='graph4', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.Row([dbc.Col([dcc.Graph(id='Ind1', className='dbc', config=config_graph)])], class_name='g-2 my-auto', style={'margin-top':'7px'}),
                dbc.Row([dbc.Col([dbc.CardBody([dcc.Graph(id='Ind2', className='dbc', config=config_graph)])])], class_name='g-2 my-auto', style={'margin-top':'7px'})
            ])
        ], sm=12, lg=4)
    ], class_name='g-2 my-auto', style={'margin-top':'7px'})
], fluid=True, style={'height':'100vh'})


# ======== CallBacks ====== #

#Graph1:
@app.callback(
    Output('graph1', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph1(toggle):

    template=template_theme1 if toggle else template_theme2

    Loja_Devolucoes=Lista_Arquivos_Concatenados.groupby(['Loja']).sum()
    Loja_Devolucoes=Loja_Devolucoes[['Quantidade Devolvida']].sort_values(by='Quantidade Devolvida', ascending=False)

    fig1 = px.bar(
        Loja_Devolucoes, x=Loja_Devolucoes.index, y='Quantidade Devolvida', 
        labels={'Quantidade Devolvida':'Quantidade Devolvida'})
    fig1.update_layout(main_config, template=template)
    fig1.update_layout({"margin": {"l":0, "r":0, "t":50, "b":0}}, height=200)
    
    return fig1

#Graph2: 
@app.callback(
    Output('graph2', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph2(toggle):

    template=template_theme1 if toggle else template_theme2

    Produto_Devolvido_Lojas = Lista_Arquivos_Concatenados.groupby('Produto').sum()
    Produto_Devolvido_Lojas=Produto_Devolvido_Lojas[['Quantidade Devolvida']].sort_values(by='Quantidade Devolvida', ascending=False)

    fig2 = px.bar(Produto_Devolvido_Lojas, x=Produto_Devolvido_Lojas.index, y='Quantidade Devolvida',
              labels={'Quantidade Devolvida':'Quantidade Devolvida'})
    fig2.update_layout(main_config, template=template)
    fig2.update_layout({"margin": {"l":0, "r":0, "t":50, "b":0}}, height=200)
    
    return fig2

# Graph 3:
@app.callback(
    Output('graph3', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph3(toggle):
    template = template_theme1 if toggle else template_theme2

    Produto_Mais_Devolvido = Lista_Arquivos_Concatenados.groupby(['Loja', 'Produto']).sum()
    Produto_Mais_Devolvido=Produto_Mais_Devolvido[['Quantidade Devolvida']].sort_values(by='Quantidade Devolvida', ascending=False)
    Produto_Mais_Devolvido=Produto_Mais_Devolvido.groupby('Loja').head(1).reset_index()

    fig3=go.Figure(go.Pie(labels=Produto_Mais_Devolvido['Loja']+'-'+Produto_Mais_Devolvido['Produto'], values=Produto_Mais_Devolvido['Quantidade Devolvida'], hole=.5))  
    fig3.update_layout(main_config, template=template, showlegend=False)
    fig3.update_layout({"margin": {"l":0, "r":0, "t":5, "b":0}}, height=200)
    
    return fig3

# Graph 4:
@app.callback(
    Output('graph4', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph4(toggle):

    template = template_theme1 if toggle else template_theme2

    Valor_Devolucoes_Loja=Lista_Arquivos_Concatenados.groupby('Loja').sum()
    Valor_Devolucoes_Loja=Valor_Devolucoes_Loja[['Preço Unitário']].sort_values(by='Preço Unitário', ascending=False)

    fig4=px.bar(Valor_Devolucoes_Loja, x=Valor_Devolucoes_Loja.index, y='Preço Unitário',
            labels={'Preço Unitário':'Preço Unitário'})
    fig4.update_layout(main_config, template=template)
    fig4.update_layout({"margin": {"l":0, "r":0, "t":50, "b":0}}, height=200)

    return fig4
    
# Graph 5:
@app.callback(
    Output('Ind1', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def Ind1(toggle):

    template=template_theme1 if toggle else template_theme2

    Loja_Devolucoes=Lista_Arquivos_Concatenados.groupby(['Loja']).sum()
    Loja_Devolucoes=Loja_Devolucoes[['Quantidade Devolvida']].sort_values(by='Quantidade Devolvida', ascending=False).reset_index()

# indicador de Loja com mais devoluções:

    Indicador1=go.Figure()
    Indicador1.add_trace(go.Indicator(
    mode='number+delta',
    title={"text": f"<span>{Loja_Devolucoes['Loja'].iloc[0]} - Store Return</span><br><span style='font-size:70%'>Store with more returns of products</span><br>"},
    value=Loja_Devolucoes['Quantidade Devolvida'].iloc[0],
    delta={'relative':True, 'reference':Loja_Devolucoes['Quantidade Devolvida'].iloc[1], 'valueformat':'.1%'}))
    

    Indicador1.update_layout(main_config, template=template)
    Indicador1.update_layout({"margin": {"l":0, "r":0, "t":50, "b":0}}, height=150)
    
    return Indicador1

# Graph 6:
@app.callback(
    Output('Ind2', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def Ind2(toggle):

    template = template_theme1 if toggle else template_theme2

    Produto_Devolvido_Lojas = Lista_Arquivos_Concatenados.groupby('Produto').sum()
    Produto_Devolvido_Lojas=Produto_Devolvido_Lojas[['Quantidade Devolvida']].sort_values(by='Quantidade Devolvida', ascending=False).reset_index()

# Indicador de produto com mais devolução:
    Indicador2=go.Figure(go.Indicator(
    mode='number+delta',
    title={"text": f"<span>{Produto_Devolvido_Lojas['Produto'].iloc[0]} - Product Return</span><br><span style='font-size:70%'>Product with more returns between products</span><br>"},
    value=Produto_Devolvido_Lojas['Quantidade Devolvida'].iloc[0],
    delta={'relative':True, 'valueformat':'.1%', 'reference':Produto_Devolvido_Lojas['Quantidade Devolvida'].iloc[1]}))  
    
    Indicador2.update_layout(main_config, template=template)
    Indicador2.update_layout({"margin": {"l":0, "r":0, "t":50, "b":0}}, height=150)

    return Indicador2
# ======== Run Sever ====== #
if __name__ == '__main__':
    app.run_server(debug=False, port=8051)