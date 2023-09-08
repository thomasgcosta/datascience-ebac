import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

sns.set() 

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[25, 10])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[25, 10])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[25, 10])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None

data = pd.read_csv('input_M15_SINASC_RO_2019.csv')
data['GESTACAO'] = data['GESTACAO'].fillna('Não Informado')

st.set_page_config(layout='wide')
st.title('Análise de dados do Sistema de Informações dos Nascidos Vivos')


data.DTNASC = pd.to_datetime(data.DTNASC)

min_data = data.DTNASC.min()
max_data = data.DTNASC.max()
gestacao = data['GESTACAO'].unique()
st.sidebar.subheader('Gestação')
gestacao_str = st.sidebar.radio(label='Semanas de gestação:',options=gestacao)
st.sidebar.divider()
st.sidebar.subheader('Data de Nascimento')
data_inicial = st.sidebar.date_input('Data inicial', 
                value = min_data,
                min_value = min_data,
                max_value = max_data)
data_final = st.sidebar.date_input('Data inicial', 
                value = max_data,
                min_value = min_data,
                max_value = max_data)  

data = data[data['GESTACAO'] == gestacao_str]
data = data[(data['DTNASC'] <= pd.to_datetime(data_final)) & (data['DTNASC'] >=pd.to_datetime(data_inicial) )]
cesareo = data[data['PARTO'] == 'Cesáreo']['PARTO'].count()
vaginal = data[data['PARTO'] == 'Vaginal']['PARTO'].count()
nascimentos = data['DTNASC'].count()

col1, col2, col3 = st.columns(3)
col1.metric("Nascimentos", nascimentos)
col2.metric("Cesária", cesareo)
col3.metric("Vaginal", vaginal)

grafico1, grafico2 = st.columns(2)
with grafico1:
    st.header('Média de peso por sexo e nascimento')
    plota_pivot_table(data, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
with grafico2:
    st.header('Média idade da mãe por nascimento')
    plota_pivot_table(data, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')

grafico3, grafico4 = st.columns(2)
with grafico3:
    st.header('Média idade da mãe por sexo e nascimento')
    plota_pivot_table(data, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
with grafico4:
    st.header('Média de peso por escolaridade da mãe')
    plota_pivot_table(data, 'PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort')
st.subheader('Mapa de municípios e nascimento')
st.map(data,latitude='munResLat', longitude='munResLon')

st.subheader('Tabela de dados')
st.dataframe(data)
