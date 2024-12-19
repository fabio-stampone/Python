import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
from PIL import Image
from io import BytesIO

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_data
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def recencia_class(x, r, q_dict):
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'

def freq_val_class(x, fv, q_dict):
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'

def main():
    st.set_page_config(
        page_title="EBAC | Módulo 31 | Streamlit V | Exercício 1",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.write("""# RFV

    RFV significa recência, frequência, valor e é utilizado para segmentação de clientes baseado no comportamento 
    de compras dos clientes e agrupa eles em clusters parecidos. Utilizando esse tipo de agrupamento podemos realizar 
    ações de marketing e CRM melhores direcionadas, ajudando assim na personalização do conteúdo e até a retenção de clientes.

    Para cada cliente é preciso calcular cada uma das componentes abaixo:

    - Recência (R): Quantidade de dias desde a última compra.
    - Frequência (F): Quantidade total de compras no período.
    - Valor (V): Total de dinheiro gasto nas compras do período.

    E é isso que iremos fazer abaixo.
    """)
    st.markdown("---")
    
    # Adicionando a lógica de upload e validações ajustadas

    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Carregue um arquivo CSV ou Excel", type=['csv', 'xlsx'])

    if data_file_1:
        try:
            if data_file_1.name.endswith('.csv'):
                df_compras = pd.read_csv(data_file_1, encoding='utf-8', infer_datetime_format=True, parse_dates=['DiaCompra'])
            elif data_file_1.name.endswith('.xlsx'):
                df_compras = pd.read_excel(data_file_1, parse_dates=['DiaCompra'])
            else:
                st.error("Formato de arquivo não suportado.")
                return
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
            return

        expected_columns = {'DiaCompra', 'ID_cliente', 'CodigoCompra', 'ValorTotal'}
        if not expected_columns.issubset(df_compras.columns):
            st.error(f"O arquivo deve conter as colunas: {', '.join(expected_columns)}")
            return

        st.write("## Análise RFV")
        dia_atual = df_compras['DiaCompra'].max()
        st.write("Dia máximo na base de dados: ", dia_atual)

        df_recencia = df_compras.groupby(by='ID_cliente', as_index=False)['DiaCompra'].max()
        df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']
        df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual - x).days)
        df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)

        df_frequencia = df_compras[['ID_cliente', 'CodigoCompra']].groupby('ID_cliente').count().reset_index()
        df_frequencia.columns = ['ID_cliente', 'Frequencia']

        df_valor = df_compras[['ID_cliente', 'ValorTotal']].groupby('ID_cliente').sum().reset_index()
        df_valor.columns = ['ID_cliente', 'Valor']

        df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
        df_RFV = df_RF.merge(df_valor, on='ID_cliente')
        df_RFV.set_index('ID_cliente', inplace=True)

        quartis = df_RFV.quantile(q=[0.25, 0.5, 0.75])
        df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class, args=('Recencia', quartis))
        df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class, args=('Frequencia', quartis))
        df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class, args=('Valor', quartis))
        df_RFV['RFV_Score'] = df_RFV['R_quartil'] + df_RFV['F_quartil'] + df_RFV['V_quartil']

        dict_acoes = {
            'AAA': 'Enviar cupons de desconto',
            'DDD': 'Churn! Fazer nada',
            'DAA': 'Enviar cupons de desconto',
            'CAA': 'Enviar cupons de desconto'
        }
        df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes)

        st.write(df_RFV.head())
        df_xlsx = to_excel(df_RFV)
        st.download_button(label='📥 Download', data=df_xlsx, file_name='RFV_Segmentacao.xlsx')

    else:
        st.info("Por favor, carregue um arquivo para começar.")

if __name__ == '__main__':
    main()
