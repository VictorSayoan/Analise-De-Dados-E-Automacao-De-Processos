
# Passo 1 -> Percorrer todos os arquivos da pasta de base de dados:
import os
import pandas as pd
import plotly.express as px

lista_arquivos_total = os.listdir(r'E:\Projetos - Análise de Dados\Indicadores_de_vendas_e_devolução\Vendas')

# Passo 2 -> Importar as bases de dados de vendas:
tabela_vendas = pd.DataFrame()  # Cria uma tabela vazia
for arquivos in lista_arquivos_total:  # Percorre todos os arquivos em lista_arquivos_total
    if "Vendas" in arquivos:
        # Ler todos os arquivos que estão na pasta Vendas com a nomenclatura Vendas:
        tabela = pd.read_csv(fr'E:\Projetos - Análise de Dados\Indicadores_de_vendas_e_devolução\Vendas\{arquivos}')
        # Atribuí estes arquivos a uma nova tabela que terá apenas os arquivos com os documentos de vendas:
        # Passo 3 -> Tratar / compilar as bases de dados:
        tabela_vendas.append(tabela)
# print()
# print(tabela_vendas)

# Passo 4 -> Calcular o produto mais vendido em quantidade:
print('Quantidade de produtos vendidos em todas as lojas: ')
tabela_quantidade_vendidos = tabela_vendas.groupby('Produto').sum()
tabela_quantidade_vendidos = tabela_quantidade_vendidos[['Quantidade Vendida']].sort_values(by='Quantidade Vendida', ascending=False)
print(tabela_quantidade_vendidos)

fig = px.bar(tabela_quantidade_vendidos, x=tabela_quantidade_vendidos.index, y='Quantidade Vendida',
             hover_data=['Quantidade Vendida', tabela_quantidade_vendidos.index], color='Quantidade Vendida',
             labels={'Qunatidade Vendida': 'Quantidade Vendida'}, height=400
             )
fig.show()

print()

# Passo 5: Calcular o produto que mais faturou
print('Faturmento em cima de cada produto de todas as lojas: ')
tabela_vendas['Faturamento'] = tabela_vendas['Quantidade Vendida'] * tabela_vendas['Preco Unitario']
tabela_faturamento = tabela_vendas.groupby('Produto').sum()
tabela_faturamento = tabela_faturamento[['Faturamento']].sort_values(by='Faturamento', ascending=False)
print(tabela_faturamento)

fig1 = px.bar(tabela_faturamento, x=tabela_faturamento.index, y='Faturamento',
              hover_data=['Faturamento', tabela_faturamento.index], color='Faturamento',
              labels={'Faturamento': 'Faturamento'}, height=400
              )
fig1.show()

print()

# Passo 6 -> Calcular a loja/cidade que mais vendeu em faturamento:
print('Ranking de lojas que mais lucraram: ')
tabela_lojas = tabela_vendas.groupby('Loja').sum()
tabela_lojas = tabela_lojas[['Faturamento']].sort_values(by='Loja', ascending=False)
print(tabela_lojas)

fig2 = px.bar(tabela_lojas, x=tabela_lojas.index, y='Faturamento',
              hover_data=['Faturamento', tabela_lojas.index],
              color='Faturamento', height=400
              )
fig2.show()

