
# Passo 1 -> Importar as bibliotecas e  percorre todos os arquivos da base de dados:

import os
import pandas as pd
import plotly.express as px

lista_total_de_arquivos = os.listdir(r'E:\Projetos - Análise de Dados\Indicadores_de_vendas_e_devolução\Vendas')
print(lista_total_de_arquivos)

# Passo 2 -> Fazer a leitura da base de dados e tratar os dados:
tabela_total = pd.DataFrame()
for arquivos in lista_total_de_arquivos:
    if 'Devolucoes' in arquivos:
        tabela_devolucao = pd.read_csv(
            fr'E:\Projetos - Análise de Dados\Indicadores_de_vendas_e_devolução\Vendas\{arquivos}'
        )
        tabela_total = tabela_total.append(tabela_devolucao)
print(tabela_total)

print()

# Passo 3 -> Encontrar o produto mais devolvido:
tabela_produto = tabela_total.groupby('Produto').sum()
tabela_produto = tabela_produto[['Quantidade Devolvida']].sort_values(by='Quantidade Devolvida', ascending=False)
print(tabela_produto)

fig1 = px.bar(tabela_produto, x=tabela_produto.index, y='Quantidade Devolvida',
              hover_data=['Quantidade Devolvida', tabela_produto.index], color='Quantidade Devolvida',
              labels={'Quantidade Devolvida': 'Quantidade Devolvida'},
              height=400
              )
fig1.show()

# Passo 4 -> Encontrar a loja que mais obteve produtos devolvidos:
tabela_lojas = tabela_total.groupby('Loja').sum()
tabela_lojas = tabela_lojas[['Quantidade Devolvida']].sort_values(by='Quantidade Devolvida', ascending=False)
print(tabela_lojas)

fig2 = px.bar(tabela_lojas, x=tabela_lojas.index, y='Quantidade Devolvida',
              hover_data=['Quantidade Devolvida', tabela_lojas.index], color='Quantidade Devolvida',
              labels={'Quantidade Devolvida': 'Quantidade devolvida por loja'},
              height=400
              )
fig2.show()
