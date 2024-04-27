import streamlit as st
import plotly.express as px

def pag1(df):
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