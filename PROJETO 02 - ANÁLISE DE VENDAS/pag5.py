import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

def pag5():
    # Carregar os dados e definir a coluna 'Data' como índice de tempo
    data = pd.read_csv("Dados_Combinados.csv", parse_dates=['Data'], index_col="Data")
    data.index=pd.to_datetime(data.index)

    # Realizar a decomposição sazonal
    decomposition = seasonal_decompose(data["Quantidade Vendida"], model='additive', period=12)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))
    decomposition.observed.plot(ax=ax1)
    ax1.set_ylabel('Observed')
    decomposition.trend.plot(ax=ax2)
    ax2.set_ylabel('Trend')
    decomposition.seasonal.plot(ax=ax3)
    ax3.set_ylabel('Seasonal')
    decomposition.resid.plot(ax=ax4)
    ax4.set_ylabel('Residual')
    plt.tight_layout()
    st.pyplot(fig)