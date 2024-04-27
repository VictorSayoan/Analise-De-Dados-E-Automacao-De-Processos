import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def pag6(df):
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
