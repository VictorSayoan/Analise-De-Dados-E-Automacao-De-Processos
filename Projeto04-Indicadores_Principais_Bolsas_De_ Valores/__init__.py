"""
Análise de dados da bolsa de Nova York.

1° Passo: Importar os arquivos

2º Passo: Análisar os dados e tratar

3º Passo: Selecionar os dados referente à bolsa de NY

4º Passo: Fazer uma análise gráfica dos dados selecionados.

OBS: Planilha tem 112.457 linhas e 8 colunas
"""
import pandas as pd
from Func_grafico import controi_grafico


# 1° Passo: Importar os arquivos

base_dados = pd.read_csv('indexData.csv', encoding='latin1')
print(base_dados)

# 2º Passo: Análisar os dados e tratá-los:

print(base_dados.info())
print(base_dados.describe())

base_dados = base_dados.dropna()  # Todos os valores vazios serão removidos da base de dados

base_dados = base_dados.rename(columns={'ï»¿Index': 'Index'})  # Renomeação da coluna index
base_dados = base_dados.rename(columns={'Volume': 'Volume de Transações'})

base_dados_atualizada = base_dados[['Index', 'Date', 'Open', 'Close', 'Volume de Transações']]
print(base_dados_atualizada)
print(base_dados_atualizada.info())

# 3º Passo: Selecionar os dados referente à bolsa de NY:

valores_excluidos = base_dados_atualizada.loc[(base_dados_atualizada[
                                                   'Index'] != 'NYA')]  # Serão selecionados os valores diferentes de Index = NYA e colocados em uma nova lista de dados
base_dados_final = base_dados_atualizada.drop(
    valores_excluidos.index)  # Da base de dados original, irei retirar os valores_excluidos atribuindo à uma nova base de dados
print(base_dados_final)

# 4º Passo: Fazer uma análise gráfica dos dados selecionados:

transacoes_maio = base_dados_final.loc[(base_dados_final['Date'] >= '2021-05-01')]
print(transacoes_maio)

controi_grafico(
    prop1=30,
    prop2=5,
    dado1=transacoes_maio['Date'],
    dado2=transacoes_maio['Open'],
    estilo='dotted',
    cor='blue',
    marcador='.',
    titulo='Graphic Date/Open', msg_x='Date', msg_y='Open'

)

controi_grafico(
    prop1=30,
    prop2=5,
    dado1=transacoes_maio['Date'],
    dado2=transacoes_maio['Close'],
    estilo='dotted',
    cor='red',
    marcador='P',
    titulo='Graphic Date/Close', msg_x='Date', msg_y='Close'

)

controi_grafico(
    prop1=30,
    prop2=5,
    dado1=transacoes_maio['Date'],
    dado2=transacoes_maio['Volume de Transações'],
    estilo='dotted',
    cor='black',
    marcador='s',
    titulo='Graphic Date/Volume de Transações', msg_x='Date', msg_y='Volume de Transações'
)

# Passo 5: Exportar base de dados analisada:

transacoes_maio.to_excel('Transações_de_Maior.xlsx', encoding='utf-8', index=False)

