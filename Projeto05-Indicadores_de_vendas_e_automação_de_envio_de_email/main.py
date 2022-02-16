# Importar base de dados:
import pandas as pd
import matplotlib.pyplot as plt
import win32com.client as win32

base_vendas = pd.read_excel('Vendas.xlsx')

print('\nVisualizar dos dados:\n')
pd.set_option('display.max_columns', None)
print(base_vendas)

print(base_vendas.info())
print(base_vendas.describe())

plt.hist(x=base_vendas['ID Loja'], y=base_vendas['Quantidade'])
plt.hist(x=base_vendas['ID Loja'], y=base_vendas['Valor Final'])

print('\nFaturamento por loja:\n')
Faturamento_total = base_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(Faturamento_total)
plt.hist(x=base_vendas['ID Loja'], y=Faturamento_total)

print('\nFaturamento médio por produto vendido por cada loja:\n')
Faturamento_medio = base_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').mean()
print(Faturamento_medio)
plt.hist(x=base_vendas['ID Loja'], y=Faturamento_medio)

print('\nQuantidade de produtos vendidos por loja:\n')
Quantidade_vendida = base_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(Quantidade_vendida)
plt.hist(x=base_vendas['ID Loja'], y=Quantidade_vendida)

print('\nTicket médio por produto vendido em cada loja:\n')
ticket_medio = (Faturamento_total['Valor Final']/Quantidade_vendida['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Médio'})
print(ticket_medio)
plt.hist(x=base_vendas['ID Loja'], y=ticket_medio)

print('\nEnviando relatório...')
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'victorfernandes0196@gmail.com'
mail.Subject = 'Relatório de Vendas por Loja'
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento total:</p>
{Faturamento_total.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Faturamento médio:</p>
{Faturamento_medio.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade Vendida:</p>
{Quantidade_vendida.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Att.,</p>
<p>Victor Sayoan</p>
'''
print('\nRelatório enviado!')
