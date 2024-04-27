import streamlit as st
import plotly.express as px

def pag3(df):
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