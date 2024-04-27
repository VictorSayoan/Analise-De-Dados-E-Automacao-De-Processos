import streamlit as st

from pag1 import pag1
from pag2 import pag2
from pag3 import pag3
from pag4 import pag4
from pag5 import pag5
from pag6 import pag6
from pag7 import pag7
from quantidade_produto import quantidade_produto
from Tratamennto_Vendas import tratatamento_vendas
from Tratamento_Devolucao import tratamento_devolucao



st.set_page_config(page_title="App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide")

df = tratatamento_vendas()
dataframe = tratamento_devolucao()


pages_principal=st.sidebar.selectbox("Selecione a opção para análise: ", ["Análise de Vendas", "Análise de Devolução"])

st.sidebar.title("Menu de Navegação")
if pages_principal == "Análise de Vendas":
    lista_de_paginas = {"Tendências de Vendas ao Longo do Tempo": "📈",
        "Desempenho do Produto": "🛍️",
        "Análise de Clientes": "👥",
        "Desempenho por Loja": "🏬",
        "Tendências Sazonais": "🌞",
        "Análise de Preço": "💰",
        "Previsão para 2019": "🔮"}

    pagina_selecionada = st.sidebar.radio("Selecione uma página", list(lista_de_paginas.keys()), index=0, format_func=lambda pagina: f"{lista_de_paginas[pagina]} {pagina}")

    match pagina_selecionada:
        case "Tendências de Vendas ao Longo do Tempo":
            pag1(df)
        case "Desempenho do Produto":
            pag2(df)
        case "Análise de Clientes":
            pag3(df)
        case "Desempenho por Loja":
            pag4(df)
        case "Tendências Sazonais":
            pag5()
        case "Análise de Preço":
            pag6(df)
        case "Previsão para 2019":
            pag7()
else:
    paginas={"Quantidade de Devoluções Por Produto": "📦"}
    
    selecao_pagina=st.sidebar.radio("Selacione uma opção: ", list(paginas.keys()), index=0, format_func=lambda pagina: f"{paginas[pagina]} {pagina}")
    
    match paginas:
        case "Quantidade de Devoluções Por Produto":
            quantidade_produto(dataframe)
    
