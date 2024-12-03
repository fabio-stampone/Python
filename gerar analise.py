import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Dicionário para mapear abreviaturas de meses para números
meses_map = {
    "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
    "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12
}

# Função para gerar gráficos e salvar pastas
def gerar_pastas_graficos(data, meses_abreviados, output_dir='C:/Users/fabio/Documents/EBAC/Modulo14/save/figs'):
    # Converter abreviaturas para números
    meses_numeros = [meses_map[mes.upper()] for mes in meses_abreviados if mes.upper() in meses_map]
    
    # Filtrar os dados para os meses especificados
    data['DTNASC'] = pd.to_datetime(data['DTNASC'], errors='coerce')
    data['MES'] = data['DTNASC'].dt.month
    dados_filtrados = data[data['MES'].isin(meses_numeros)]
    
    # Criar a pasta de saída
    os.makedirs(output_dir, exist_ok=True)
    
def plota_pivot_table(data, values, index, aggfunc, title, xlabel, unstack=False, sort=False, output_name=None):
    pivot = data.pivot_table(values=values, index=index, aggfunc=aggfunc)
    if unstack:
        pivot = pivot.unstack()
    if sort:
        pivot = pivot.sort_values(by=values if not unstack else list(pivot.columns), ascending=True)
    
    # Selecionar apenas colunas numéricas
    pivot = pivot.apply(pd.to_numeric, errors='coerce').dropna()
    
    # Verificar se os dados são numéricos
    if pivot.empty or not pivot.select_dtypes(include='number').shape[1]:
        print(f"Erro: Nenhum dado numérico disponível para o gráfico '{title}'.")
        return
    
    pivot.plot(kind='bar' if not unstack else 'barh', figsize=(10, 6))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(values)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Salvar o gráfico
    if output_name:
        plt.savefig(os.path.join(output_dir, output_name))
    plt.show()
    
    # Gerar os gráficos
    plota_pivot_table(
        dados_filtrados, 'IDADEMAE', 'DTNASC', 'count', 
        'Contagem da Idade das Mães ao Longo do Tempo', 
        'Data de Nascimento', 
        output_name='contagem_idade_mae.png'
    )
    plota_pivot_table(
        dados_filtrados, 'PESO', ['MES', 'SEXO'], 'mean', 
        'Média de Peso dos Bebês por Sexo e Mês', 
        'Mês', unstack=True, 
        output_name='media_peso_sexo.png'
    )
    plota_pivot_table(
        dados_filtrados, 'PESO', 'ESCMAE', 'mean', 
        'Peso Médio dos Bebês por Escolaridade da Mãe', 
        'Escolaridade', sort=True, 
        output_name='peso_escolaridade.png'
    )
    print(f"Gráficos gerados e salvos na pasta: {output_dir}")

# Main para rodar o script
if __name__ == "__main__":
    # Exemplo: python script.py MAR ABR MAI JUN DEZ
    args = sys.argv[1:]  # Lista de abreviaturas de meses recebida como argumento
    if not args:
        print("Por favor, forneça uma lista de abreviaturas de meses (ex.: MAR ABR MAI).")
        sys.exit(1)
    
    # Carregar a base de dados
    file_path = 'C:/Users/fabio/Documents/EBAC/Modulo14/input/SINASC_RO_2019.csv'  # Substitua pelo caminho correto do arquivo
    data = pd.read_csv(file_path)
    
    # Gerar gráficos para os meses fornecidos
    gerar_pastas_graficos(data, args)
