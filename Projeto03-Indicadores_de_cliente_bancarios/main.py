import pandas as pd
import plotly.express as px

# Passo 1 -> Importação da base de dados:

Base_dados = pd.read_csv('ClientesBanco.csv', encoding='latin1')
print(Base_dados)

# Passo 2 -> Análise e tratamento dos dados:

"""
Como não será necessário para a análise a coluna de CLIENTNUM, irei exclui-lá:
"""

Base_dados = Base_dados.drop('CLIENTNUM', axis=1)
print(Base_dados.info())
print()

"""
Como temos um valor nulo na coluna de Categoria Cartão, é necessário retirá-lo da análise, já que não irá interferir 
nesta:
"""

Base_dados = Base_dados.dropna()
print(Base_dados.info())

"""
É necessário saber a quantidade de pessoas que são cliente e quantidade de pessoas que cancelaram:
"""
print()
Base_dados.describe()

contagem_valores_categoria = Base_dados['Categoria'].value_counts()
print(contagem_valores_categoria)
print()
perc_cont_categoria = Base_dados['Categoria'].value_counts(normalize=True)
print(perc_cont_categoria*100)

"""
De acordo com a análise feita, temos 8499 clientes ativos e 1627 clientes cancelados, 
ou seja, os clientes cancelados representam 16% do total de clientes.
Necessário uma análise do motivo pelo qual temos um alto número de cancelamentos.
"""

# Passo 3: Análise gráfico:

"""
Esta parte do código irá realizar a análise comparativa de cada coluna em relação à categoria: 
"""
for dados in Base_dados:
    grafico = px.histogram(Base_dados, x=dados, color='Categoria')
    grafico.show()

"""
Detalhes dos gráficos:
1°:     Em relação à idade por cancelamento, temos que o cancelamento ocorre entre pessoa que tenham entre 40 e 55, 
então podemos não estar atendendo a esta demanda.
2°:     Podemos observar que a maioria dos cancelamentos estão na categoria cartão blue, ou seja, temos um total 
de 1519 cancelamentos nesta categoria do cartão, tendo em vista que temos 1627 cancelamentos ao total.
3°:     Quanto maior a quantidade de produtos adquiridos pelo cliente, menor a chance de termos cancelamentos.
4°:     Clientes que passam 2 ou 3 meses inativos tendem a cancelar.
5°:     Quanto maior a quantidade de contatos feitos pelo cliente com a nossa equipe de TeleMarketing, 
maior a chance deste cancelar.
6°:     Clientes com o limite de transações mais baixo tendem a cancelar com mais facilidade, limite até 5k.
7°:     Clientes que fizeram até 3k em valor de transação até 12 meses tendem a cancelar.
8°:     Clientes que realizam entre 30 e 50 transações dentro de 12 meses tendem a cancelar com mais facilidade.
9°:     Quanto maior a taxa de utilzação do cartão, menor a chance dos clientes cancelarem.

"""


