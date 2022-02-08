# Passo 1: Importar as bibliotecas e fazer a leitura dos dados:
import pandas as pd
import seaborn as sns

base_dados = pd.read_csv('t1.csv')

# Passo 2 -> Tratar os dados:
print(base_dados.info())

base_dados['Date/Time'] = pd.to_datetime(base_dados['Date/Time'])
del base_dados['Wind Direction (°)']
print(base_dados)

# Passo 3 -> Análise gráfica da potêcia ativa:
# -->  Em relação à velocidade do vento:
sns.scatterplot(data=base_dados, x='Wind Speed (m/s)', y='LV ActivePower (kW)')


# Passo 4 -> Análise gráfica da potência teórica:
# --> Em relação à velocidade do vento:
sns.scatterplot(data=base_dados, x='Wind Speed (m/s)', y='Theoretical_Power_Curve (KWh)')

# Passo 5 -> Estabelecimento de um limite de 5% para a potância usual:
potencia_real = base_dados['LV ActivePower (kW)'].tolist()
potencia_teorica = base_dados['Theoretical_Power_Curve (KWh)'].tolist()
potencia_maxima = []
potencia_minima = []

for dados in potencia_teorica:
    potencia_maxima.append(round(dados*1.05, 2))     # Adiciona um valor de 5% para cima
    potencia_minima.append(round(dados*0.95, 2))  # Adiciona um valor de 5% para baixo

base_dados['Potencia Máxima'] = potencia_maxima
base_dados['Potência Mínima'] = potencia_minima

# Passo 6 -> Criar uma coluna informando se o dado está dentro ou fora do limite:
# Verificar se a potência real está dentro do limite da potência teórica:
No_Limite = []
for p, potencia in enumerate(potencia_real):
    if potencia >= potencia_minima[p] and potencia <= potencia_maxima[p]:
        No_Limite.append('Dentro do limite')
    elif potencia == 0:
        No_Limite.append('Nao gerou potencia')
    else:
        No_Limite.append('Fora do limite')

base_dados['Limite Permitido'] = No_Limite

# Passo 7 -> Plotar o gráfico da análise total:
cores = {'Dentro do limite': 'blue',
         'Nao gerou potencia': 'orange',
         'Fora do limite': 'red'}

sns.scatterplot(data=base_dados, x='Wind Speed (m/s)',
                y='LV ActivePower (kW)',
                hue='Limite Permitido',
                s=1,
                palette=cores)

