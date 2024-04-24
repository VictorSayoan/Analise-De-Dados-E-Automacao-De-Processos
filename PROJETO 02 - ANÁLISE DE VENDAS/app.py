import pandas as pd
import numpy as np
import os
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from statsmodels.tsa.seasonal import seasonal_decompose

def pag1():
    # Tendências de Vendas ao Longo do Tempo:
    col1, col2 = st.columns(2)
    with col1:
        opcao_analise=st.radio("Selecione a métrica para análise: ", ("Quantidade de Vendas", "Receita Total"))
    with col2:
        intervalo_de_tempo=st.radio("Selecione o intervalo de tempo: ", ("Mensal", "Trimestral"))

    if intervalo_de_tempo == "Mensal":
        dados_agrupados = df.resample('M').sum()
    else:
        dados_agrupados = df.resample('Q').sum()
    
    if opcao_analise == "Quantidade de Vendas":
        fig = px.line(dados_agrupados, x=dados_agrupados.index, y='Quantidade Vendida', title='Tendências de Vendas ao Longo do Tempo')
        st.plotly_chart(fig)
    else:
        fig = px.line(dados_agrupados, x=dados_agrupados.index, y=dados_agrupados['Quantidade Vendida'] * dados_agrupados['Preco Unitario'], title='Tendências de Receita ao Longo do Tempo')
        st.plotly_chart(fig)
def pag2():
    opcao=st.selectbox("Selecione a métrica de análise", 
                       ['Total Unidades Vendidas', 'Preco Medio', 'Receita Total', 'Preco Minimo', 'Preco Maximo'], 
                       index=0)
    match opcao:
        case 'Total Unidades Vendidas':
            desempenho_produto = df.groupby(["Produto"])["Quantidade Vendida"].sum().reset_index()
            desempenho_produto = desempenho_produto.sort_values(by="Quantidade Vendida", ascending=False)
            figure1 = px.bar(desempenho_produto, x="Produto", y="Quantidade Vendida",
                     color="Produto")
            st.title("Análise de Desempenho Por Quantidade de Produto Vendido: ")
            st.plotly_chart(figure1,use_container_width=True)
        case 'Preco Medio':
            # Calcule o preço médio de venda para cada produto e veja se há variações significativas. 
            # Isso pode ajudar a ajustar a estratégia de preços.
            preco_medio=df.groupby(["Produto"])["Preco Unitario"].mean().reset_index()
            preco_medio = preco_medio.sort_values(by="Produto", ascending=False)
            figure2 = px.bar(preco_medio, x="Produto", y="Preco Unitario",
                              color="Produto")
            st.title("Análise de Desempenho Por Preço Médio")
            st.plotly_chart(figure2, use_container_width=True)
        case "Receita Total":
            data = df.groupby(["Produto", "Preco Unitario"])["Quantidade Vendida"].sum().reset_index()
            data['Receita Total'] = data["Preco Unitario"]*data["Quantidade Vendida"].round(2)
            figure3 = px.bar(data, x="Produto", y="Receita Total",
                             color="Produto")
            st.title("Análise de Produtos Por Receita Total")
            st.plotly_chart(figure3, use_container_width=True)
        case "Preco Minimo":
            df_minimo = df.groupby(["Produto"])["Preco Unitario"].min().reset_index()
            df_minimo=df_minimo.rename(columns={"Preco Unitario":"Preco Minimo"})
            df_minimo.set_index("Produto", inplace=True)
            figure4=px.line(df_minimo, x=df_minimo.index, y="Preco Minimo")
            st.title("Preço Mínimo Por Produto: ")
            st.plotly_chart(figure4, use_container_width=True)
        case "Preco Maximo":
            df_maximo=df.groupby(["Produto"])["Preco Unitario"].max().reset_index()
            df_maximo=df_maximo.rename(columns={"Preco Unitario":"Preco Maximo"})
            figure5=px.bar(df_maximo, x="Produto", y="Preco Maximo", color="Produto")
            st.title("Preço Máximo Por Produto: ")
            st.plotly_chart(figure5, use_container_width=True)

def pag3():
    # Descubra quem são os clientes mais frequentes e quem gasta mais. 
    #Isso pode ajudar a segmentar melhor o mercado e direcionar campanhas de marketing específicas.
    opcao=st.selectbox("Selecione a métrica analisada: ", ["Quantidade Vendida", "Valor Investido"])
    if opcao=="Quantidade Vendida":
        quantidade_clientes=df.groupby(["Primeiro Nome", "Sobrenome"])["Quantidade Vendida"].sum().reset_index()
        quantidade_clientes=quantidade_clientes.sort_values(by="Quantidade Vendida", ascending=False)
        quantidade_clientes["Nome Completo"] = quantidade_clientes["Primeiro Nome"] + ' ' + quantidade_clientes["Sobrenome"]
        vinte_quantidade_clientes=quantidade_clientes.head(30)
        fig1 = px.bar(vinte_quantidade_clientes, x="Nome Completo", y="Quantidade Vendida", color="Nome Completo")
        st.title("Os 30 melhores compradores: ")
        st.plotly_chart(fig1, use_container_width=True)
    else:
        valor_clientes = df.groupby(["Primeiro Nome", "Sobrenome"])["Preco Unitario"].sum().reset_index()
        valor_clientes=valor_clientes.sort_values(by="Preco Unitario", ascending=False)
        valor_clientes["Nome Completo"] = valor_clientes["Primeiro Nome"] + ' ' + valor_clientes["Sobrenome"]
        valor_clientes=valor_clientes.rename(columns={"Preco Unitario":"Valor Comprado em R$"})
        vinte_valor_clientes=valor_clientes.head(30)
        fig2=px.bar(vinte_valor_clientes, x="Nome Completo", y="Valor Comprado em R$", color="Nome Completo")
        st.title("Os 20 melhores compradores: ")
        st.plotly_chart(fig2, use_container_width=True)

def pag4():
    desempenho_loja=df.groupby(["Loja"]).agg({"Quantidade Vendida": "sum", 
                                              "Preco Unitario":"mean"}).reset_index()
    desempenho_loja["Receita Total"] = desempenho_loja["Preco Unitario"] * desempenho_loja["Quantidade Vendida"]
    desempenho_loja.set_index("Loja", inplace=True)
    desempenho_loja=desempenho_loja.sort_values(by="Receita Total", ascending=False)

    figure1=px.line(desempenho_loja, x=desempenho_loja.index, y="Receita Total")
    st.title("Desempenho por Receita Total: ")
    st.plotly_chart(figure1, use_container_width=True)

def pag5():
    # Carregar os dados e definir a coluna 'Data' como índice de tempo
    data = pd.read_csv("Dados_Combinados.csv", parse_dates=['Data'], index_col="Data")
    data.index=pd.to_datetime(data.index)

    # Realizar a decomposição sazonal
    decomposition = seasonal_decompose(data["Quantidade Vendida"], model='additive', period=12)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))
    decomposition.observed.plot(ax=ax1)
    ax1.set_ylabel('Observed')
    decomposition.trend.plot(ax=ax2)
    ax2.set_ylabel('Trend')
    decomposition.seasonal.plot(ax=ax3)
    ax3.set_ylabel('Seasonal')
    decomposition.resid.plot(ax=ax4)
    ax4.set_ylabel('Residual')
    plt.tight_layout()
    st.pyplot(fig)

def pag6():
    # Análise de quantidade vendida por lojas:
    data_frame=df.groupby(["Loja", "Produto", "Preco Unitario"])["Quantidade Vendida"].sum().reset_index()
    data_frame["Receita Por Produto"]=(data_frame["Preco Unitario"] * data_frame["Quantidade Vendida"]).round(2)
    data_frame.to_csv("analise_preco", index=False)
    data = pd.read_csv("analise_preco", parse_dates=['Loja'], index_col="Loja")
    
    opcoes_loja = ["Belo Horizonte", "Curitiba", "Fortaleza", "Goiás", "Porto Alegre",  
                   "Recife", "Rio de Janeiro", "Salvador", "São Paulo"]
    
    opcao=st.selectbox("Selecione a loja para análise: ", opcoes_loja)
    if opcao:
        dados_filtrados=data.loc[opcao]
        
        st.subheader(f'Análise de Quantidade Vendida para {opcao}')
        figure=go.Figure(go.Bar(x=dados_filtrados["Produto"], y=dados_filtrados["Quantidade Vendida"], name="Quantidade Vendida"))
        figure.update_layout(barmode='group', xaxis_tickangle=-45, title=f'Análise para {opcao}')
        st.plotly_chart(figure, use_container_width=True)

        st.subheader(f'Análise de Receita Total Por Produto para {opcao}')
        figure1=go.Figure(go.Bar(x=dados_filtrados["Produto"], y=dados_filtrados["Receita Por Produto"], name="Receita Total Por Produto"))
        figure1.update_layout(barmode='group', xaxis_tickangle=-45, title=f'Análise para {opcao}')
        st.plotly_chart(figure1, use_container_width=True)

def pag7():
    pass

st.set_page_config(page_title="App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide")

Dados_Vendas=[]

directory = r'D:\OneDrive\SAYOAN\01- PORTFÓLIO - ANÁLISE DE DADOS\PROJETO 04\Vendas'
Lista_Arquivos = os.listdir(directory)

for arquivos in Lista_Arquivos:
    if "Vendas" in arquivos:
        Dados=pd.read_csv(os.path.join(directory, arquivos))
        Dados_Vendas.append(Dados)

Dados_combinados=pd.concat(Dados_Vendas)
Dados_combinados.to_csv("Dados_Combinados.csv", index=False)

df = pd.read_csv(r'Dados_Combinados.csv')

#Tratamento dos dados:
df['Data']=pd.to_datetime(df["Data"])
df.set_index('Data', inplace=True)

df['Month']=df.index.month
df = df.sort_values(by="Month")
df['Preco Unitario'] = pd.to_numeric(df["Preco Unitario"])

lista_de_paginas = {"Tendências de Vendas ao Longo do Tempo": "📈",
    "Desempenho do Produto": "🛍️",
    "Análise de Clientes": "👥",
    "Desempenho por Loja": "🏬",
    "Tendências Sazonais": "🌞",
    "Análise de Preço": "💰",
    "Previsão para 2019": "🔮"}

st.sidebar.title("Menu de Navegação")
pagina_selecionada = st.sidebar.radio("Selecione uma página", list(lista_de_paginas.keys()), index=0, format_func=lambda pagina: f"{lista_de_paginas[pagina]} {pagina}")

match pagina_selecionada:
    case "Tendências de Vendas ao Longo do Tempo":
        pag1()
    case "Desempenho do Produto":
        pag2()
    case "Análise de Clientes":
        pag3()
    case "Desempenho por Loja":
        pag4()
    case "Tendências Sazonais":
        pag5()
    case "Análise de Preço":
        pag6()
    case "Previsão para 2019":
        pag7()
