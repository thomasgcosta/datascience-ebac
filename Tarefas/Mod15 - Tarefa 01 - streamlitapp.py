import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

sns.set()  

data = pd.read_csv('input_M15_SINASC_RO_2019.csv')
data['GESTACAO'] = data['GESTACAO'].fillna('Não Informado')

st.set_page_config(layout='wide')
st.title('Análise de dados do Sistema de Informações dos Nascidos Vivos')
st.subheader('Tabela de dados')

data.DTNASC = pd.to_datetime(data.DTNASC)

min_data = data.DTNASC.min()
max_data = data.DTNASC.max()
gestacao = data['GESTACAO'].unique()
gestacao_str = st.sidebar.radio('Gestação:', gestacao)
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

st.write(data.shape)
st.dataframe(data)