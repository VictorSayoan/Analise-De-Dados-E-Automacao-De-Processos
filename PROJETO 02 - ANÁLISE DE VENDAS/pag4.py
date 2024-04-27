import streamlit as st
import plotly.express as px

def pag4(df):
    desempenho_loja=df.groupby(["Loja"]).agg({"Quantidade Vendida": "sum", 
                                              "Preco Unitario":"mean"}).reset_index()
    desempenho_loja["Receita Total"] = desempenho_loja["Preco Unitario"] * desempenho_loja["Quantidade Vendida"]
    desempenho_loja.set_index("Loja", inplace=True)
    desempenho_loja=desempenho_loja.sort_values(by="Receita Total", ascending=False)

    figure1=px.line(desempenho_loja, x=desempenho_loja.index, y="Receita Total")
    st.title("Desempenho por Receita Total: ")
    st.plotly_chart(figure1, use_container_width=True)