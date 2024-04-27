# Análise de dados para as devoluções:
import os
import pandas as pd

def tratamento_devolucao():
    Dados_Devolucao=[]

    directory2=r'D:\OneDrive\SAYOAN\01- PORTFÓLIO - ANÁLISE DE DADOS\PROJETO 04\Devolucoes'
    lista_devolucao=os.listdir(directory2)

    for arquivos2 in lista_devolucao:
        if "Devolucoes" in arquivos2:
            Dados2=pd.read_csv(os.path.join(directory2, arquivos2))
            Dados_Devolucao.append(Dados2)

    Combinados_devolucao=pd.concat(Dados_Devolucao)
    Combinados_devolucao.to_csv("Dados_Combinados_Devolucao.csv")

    dataframe=pd.read_csv(r"Dados_Combinados_Devolucao.csv")

    #Tratamento dos dados:
    dataframe['Data']=pd.to_datetime(dataframe['Data'])
    dataframe.set_index('Data', inplace=True)

    dataframe['Month']=dataframe.index.month
    dataframe=dataframe.sort_values(by='Month')

    return dataframe

#                  Fim          #