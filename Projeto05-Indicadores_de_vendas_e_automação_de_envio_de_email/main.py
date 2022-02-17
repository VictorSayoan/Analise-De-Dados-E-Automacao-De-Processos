import pandas as pd
import plotly.express as px
import win32com.client as win32

base_vendas = pd.read_excel('Vendas.xlsx')

print('\nVisualizar dos dados:\n')
pd.set_option('display.max_columns', None)
base_vendas = base_vendas.rename(columns={'ID Loja': 'ID_loja'})
print(base_vendas)

print(base_vendas.info())
print(base_vendas.describe())

print('\nFaturamento por loja:\n')
Faturamento_total = base_vendas[['ID_loja', 'Valor Final']].groupby('ID_loja').sum()
print(Faturamento_total)

fig1 = px.bar(Faturamento_total, x=Faturamento_total.index, y='Valor Final',
               hover_data=['Valor Final', Faturamento_total.index], color='Valor Final', height=400)
fig1.show()

print('\nFaturamento médio por produto vendido por cada loja:\n')
Faturamento_medio = base_vendas[['ID_loja', 'Valor Final']].groupby('ID_loja').mean()
print(Faturamento_medio)
fig2 = px.bar(Faturamento_medio, x=Faturamento_medio.index, y='Valor Final',
              hover_data=['Valor Final', Faturamento_medio.index],
              color='Valor Final',
              height=400)
fig2.show()


print('\nQuantidade de produtos vendidos por loja:\n')
Quantidade_vendida = base_vendas[['ID_loja', 'Quantidade']].groupby('ID_loja').sum()
print(Quantidade_vendida)
fig3 = px.bar(Quantidade_vendida, x=Quantidade_vendida.index, y='Quantidade',
              hover_data=['Quantidade', Quantidade_vendida.index],
              color='Quantidade',
              height=400)
fig3.show()

print('\nTicket médio por produto vendido em cada loja:\n')
ticket_medio = (Faturamento_total['Valor Final'] / Quantidade_vendida['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Médio'})
print(ticket_medio)
fig4 = px.bar(ticket_medio, x=ticket_medio.index, y='Ticket Médio', hover_data=['Ticket Médio', ticket_medio.index],
              color='Ticket Médio', height=400)
fig4.show()


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

anexo1 = r'E:\Projetos - Análise de Dados\Projeto07-Indicadores_de_vendas_e_automação_de_envio_de_email\imagens\
Faturamento_Total'
anexo2 = r'E:\Projetos - Análise de Dados\Projeto07-Indicadores_de_vendas_e_automação_de_envio_de_email\imagens\
Faturamento_medio'
anexo3 = r'E:\Projetos - Análise de Dados\Projeto07-Indicadores_de_vendas_e_automação_de_envio_de_email\imagens\
Quantidade_vendida'
anexo4 = r'E:\Projetos - Análise de Dados\Projeto07-Indicadores_de_vendas_e_automação_de_envio_de_email\imagens\
Ticket_medio'
mail.Attachments.Add(anexo1)
mail.Attachments.Add(anexo2)
mail.Attachments.Add(anexo3)
mail.Attachments.Add(anexo4)
mail.Send()
print('\nRelatório enviado!')
