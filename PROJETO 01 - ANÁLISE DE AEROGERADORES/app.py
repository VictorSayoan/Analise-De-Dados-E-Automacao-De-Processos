import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Leitura dos dados:
df = pd.read_csv(r'T1.csv')

def pag1():
    # Relação entre  a velocidade do vento e a potência ativa gerada:
    figure1 = px.scatter(df, x="Wind Speed (m/s)", y="LV ActivePower (kW)",
                        opacity=0.5,
                        color="Wind Speed (m/s)")
    st.title("Gráfico de Dispersão: Potência Ativa vs. Velocidade do Vento")
    st.plotly_chart(figure1, use_container_width=True)

    correlation = df["Wind Speed (m/s)"].corr(df["LV ActivePower (kW)"])
    if correlation >= -1 and correlation < 0:
        st.write("As variavéis possuim alta correlação negativa!")
    elif correlation > 0 and correlation <= 1:
        st.write("As variáveis possuem alta correlação positiva!")
    else:
        st.write("As variáveis não possuem correlação")
    
    # Relação entre potência ativa e a direção do vento (Wind Direction):
    figure2 = px.scatter(df, x="Wind Direction (°)", y="LV ActivePower (kW)",
                         opacity=0.5, color="Wind Direction (°)")
    st.title("Gráfico de Dispersão: Potência Ativa vs. Direção do Vento")
    st.plotly_chart(figure2, use_container_width=True)

    correlation_Direction_Active = df["Wind Speed (m/s)"].corr(df["LV ActivePower (kW)"])
    if correlation_Direction_Active >= -1 and correlation_Direction_Active < 0:
        st.write("As variavéis possuim alta correlação negativa!")
    elif correlation_Direction_Active > 0 and correlation_Direction_Active <= 1:
        st.write("As variáveis possuem alta correlação positiva!")
    else:
        st.write("As variáveis não possuem correlação", text_align="center")

def pag2():
    figure3, ax = plt.subplots(figsize=(10, 6)) 
    ax.plot(df["Wind Speed (m/s)"], df["LV ActivePower (kW)"], label="Potência Ativa Real", color="blue")
    ax.plot(df["Wind Speed (m/s)"], df["Theoretical_Power_Curve (KWh)"], label="Potência Ativa Teórica", color="red")
    ax.set_xlabel('Velocidade do Vento (m/s)', color="white")
    ax.set_ylabel('Potência (kW)', color="white")
    ax.legend(loc='lower right', fontsize='large', shadow=True)
    ax.grid(True)
    st.title('Comparação entre Potência Ativa e Curva de Potência Teórica')
    st.plotly_chart(figure3, use_container_width=True)

def pag3():
    # Análise Temporal da potência ativa em relação ao tempo:
    # Análise de Potência Ativa Por mês:
    df_mes_potencia = df.groupby("Month")["LV ActivePower (kW)"].sum().reset_index()
    
    figure4 = px.bar(df_mes_potencia, x="Month", y="LV ActivePower (kW)",
                     color="LV ActivePower (kW)")
    st.title("Geração de Energia: Potência Ativa vs. Mês")
    st.plotly_chart(figure4, use_container_width=True)

def pag4():
    mean_prooduction = df.groupby("Month")["LV ActivePower (kW)"].mean().reset_index().round(2)

    # Ajusta uma linha de regressão:
    X = mean_prooduction["Month"].values.reshape(-1,1)
    Y = mean_prooduction['LV ActivePower (kW)'].values.reshape(-1,1)
    reg = LinearRegression().fit(X, Y)

    # Realiza as previsões da Regressão Linear:
    predictions = reg.predict(X)

    figure6, ax = plt.subplots(figsize=(10,6))
    ax.scatter(mean_prooduction["Month"],mean_prooduction['LV ActivePower (kW)'], color='blue', label='Dados Reais')
    ax.plot(mean_prooduction["Month"], predictions, color='red', linewidth=2, label='Regressão Linear')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Potência Ativa Média (kW)')
    ax.legend()
    ax.grid(True)
    st.title("Regressão Linear da Potência Ativa Média ao Longo dos Meses")
    st.pyplot(figure6, use_container_width=True)
    
def pag5():
    bins = [0, 5, 10, 15, 20, 25, 30, float('inf')]
    labels = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30+']

    df['wind_speed_category'] = pd.cut(df['Wind Speed (m/s)'], bins=bins, labels=labels)
    mean_power_by_speed_wind = df.groupby('wind_speed_category')['LV ActivePower (kW)'].mean().reset_index().round(2)
    
    st.title('Desempenho da Turbina Eólica por Faixa de Velocidade do Vento')
    st.bar_chart(mean_power_by_speed_wind.set_index('wind_speed_category'), color='LV ActivePower (kW)')

def pag6():
    bins = [0, 50, 100, 250, 300, 350, float('inf')]
    labels = ['0-50', '50-100', '100-150', '150-200', '200-250', '250-300']

    df['direction_wind_category']=pd.cut(df['Wind Direction (°)'], bins=bins, labels=labels)
    mean_power_by_direction_wind=df.groupby('direction_wind_category')['LV ActivePower (kW)'].mean().reset_index().round(2)
    
    st.title('Desempenho da Turbina Eólica por Faixa de Direção do Vento')
    st.bar_chart(mean_power_by_direction_wind.set_index('direction_wind_category'), color='LV ActivePower (kW)')


st.set_page_config(layout="wide", page_title="Análise de Qualidade de Energia", page_icon="📊")

# Tratamento dos dados:
df["Date/Time"]=pd.to_datetime(df["Date/Time"], format="%d %m %Y %H:%M")
df["Month"] = df["Date/Time"].dt.month

pages = st.selectbox("Selecone a aba de analise", ["Correlação entre variáveis", "Comparação com a teoria", 
                                                   "Análise temporal", "Análise de tendências", 
                                                   "Análise de desempenho em diferentes velocidades do vento",
                                                   "Análise de desempenho em diferentes direções do vento"],
                                                   index=0)
match pages:
    case "Correlação entre variáveis":
        pag1()
    case "Comparação com a teoria":
        pag2()
    case"Análise temporal":
        pag3()
    case "Análise de tendências":
        pag4()
    case "Análise de desempenho em diferentes velocidades do vento":
        pag5()
    case "Análise de desempenho em diferentes direções do vento":
        pag6()
