import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import datetime

# Título da aplicação
st.title('Demonstração de Recursos do Streamlit')

# 1. Exibir texto simples
st.text('Este é um texto simples exibido com st.text.')

# 2. Exibir texto em Markdown
st.markdown('**Este é um texto em negrito usando Markdown.**')

# 3. Exibir código com destaque de sintaxe
code = '''def saudacao(nome):
    return f"Olá, {nome}!"'''
st.code(code, language='python')

# 4. Exibir LaTeX
st.latex(r'\int_a^b f(x)dx')

# 5. Exibir JSON formatado
st.json({'chave': 'valor', 'lista': [1, 2, 3]})

# 6. Exibir uma tabela de dados
df = pd.DataFrame({
    'Coluna 1': [1, 2, 3, 4],
    'Coluna 2': [10, 20, 30, 40]
})
st.table(df)

# 7. Exibir um gráfico de linha simples
st.line_chart(df)

# 8. Exibir um gráfico de área simples
st.area_chart(df)

# 9. Exibir um gráfico de barras simples
st.bar_chart(df)

# 10. Exibir um gráfico Altair
chart = alt.Chart(df).mark_bar().encode(
    x='Coluna 1',
    y='Coluna 2'
)
st.altair_chart(chart, use_container_width=True)

# 11. Exibir um gráfico Plotly
fig = px.line(df, x='Coluna 1', y='Coluna 2', title='Gráfico Plotly')
st.plotly_chart(fig)

# 12. Exibir um mapa com pontos
map_data = pd.DataFrame({
    'lat': [37.76, 37.77, 37.78],
    'lon': [-122.4, -122.41, -122.42]
})
st.map(map_data)

# 13. Exibir um slider
numero = st.slider('Selecione um número', 0, 100, 50)
st.write(f'Número selecionado: {numero}')

# 14. Exibir uma caixa de seleção
if st.checkbox('Mostrar gráfico de Matplotlib'):
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [10, 20, 30])
    st.pyplot(fig)

# 15. Exibir uma caixa de seleção múltipla
opcoes = st.multiselect(
    'Quais são suas cores favoritas?',
    ['Verde', 'Amarelo', 'Vermelho', 'Azul'],
    ['Verde', 'Azul']
)
st.write('Você selecionou:', opcoes)

# 16. Exibir uma caixa de seleção única
animal = st.radio(
    'Qual é o seu animal favorito?',
    ['Gato', 'Cachorro', 'Pássaro']
)
st.write('Você gosta de:', animal)

# 17. Exibir uma entrada de texto
nome = st.text_input('Digite seu nome')
st.write(f'Olá, {nome}!')

# 18. Exibir uma área de texto
mensagem = st.text_area('Digite uma mensagem')
st.write('Sua mensagem:', mensagem)

# 19. Exibir uma entrada de data
data = st.date_input('Selecione uma data', datetime.date.today())
st.write('Data selecionada:', data)

# 20. Exibir uma entrada de hora
hora = st.time_input('Selecione um horário', datetime.time(8, 0))
st.write('Horário selecionado:', hora)
