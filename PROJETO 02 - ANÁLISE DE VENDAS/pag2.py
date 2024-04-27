import streamlit as st
import plotly.express as px

def pag2(df):
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
