import plotly.graph_objects as go
import streamlit as st

def quantidade_produto(dataframe):
    quant_devol=dataframe.groupby(['Loja', 'Produto'])['Quantidade Devolvida'].sum().reset_index()
    quant_devol=quant_devol.set_index('Loja')
    
    opcao_loja=["Belo Horizonte", "Curitiba", "Fortaleza", "Goiás", "Porto Alegre",  
                   "Recife", "Rio de Janeiro", "Salvador", "São Paulo"]
    opcao_loja=st.selectbox('Selecione a loja para análise: ', opcao_loja)

    if opcao_loja:
        dados_filtrados=quant_devol.loc[opcao_loja]
        
        st.subheader(f'Análise da Quantidade de Prdutos Devolvidos para {opcao_loja}')
        figure=go.Figure(go.Bar(x=dados_filtrados["Produto"], y=dados_filtrados["Quantidade Devolvida"], name="Quantidade Devolvida"))
        figure.update_layout(barmode='group', xaxis_tickangle=-45, title=f'Análise para {opcao_loja}')
        st.plotly_chart(figure, use_container_width=True)