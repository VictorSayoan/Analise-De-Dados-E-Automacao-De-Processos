# Análise de dados para as vendas:
import os
import pandas as pd

def tratatamento_vendas():
    Dados_Vendas=[]

    directory = r'D:\OneDrive\SAYOAN\01- PORTFÓLIO - ANÁLISE DE DADOS\PROJETO 04\Vendas'
    Lista_Arquivos = os.listdir(directory)

    for arquivos in Lista_Arquivos:
        if "Vendas" in arquivos:
            Dados=pd.read_csv(os.path.join(directory, arquivos))
            Dados_Vendas.append(Dados)

    Dados_combinados=pd.concat(Dados_Vendas)
    Dados_combinados.to_csv("Dados_Combinados.csv", index=False)

    df = pd.read_csv(r'Dados_Combinados.csv')

    #Tratamento dos dados:
    df['Data']=pd.to_datetime(df["Data"])
    df.set_index('Data', inplace=True)

    df['Month']=df.index.month
    df = df.sort_values(by="Month")
    df['Preco Unitario'] = pd.to_numeric(df["Preco Unitario"])

    return df
#               Fim             #