# Biblioteca utilizada: PDF Kit (pip intall pdfkit)
# Necessário baixar o wkhtmltopdf e colocar no PATH

import os
import pdfkit

# Defina o caminho completo para o executável wkhtmltopdf
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Configure pdfkit para usar este caminho
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# Caminho da pasta onde estão os arquivos HTML
input_folder = r'C:\Users\fabio.stampone\Documents\PDF Metrics\HTML Entrada'

# Caminho da pasta onde os arquivos PDF serão salvos
output_folder = r'C:\Users\fabio.stampone\Documents\PDF Metrics\PDF Saida'

# Crie a pasta de saída se não existir
os.makedirs(output_folder, exist_ok=True)

# Opções para uma página A4 com margens comuns
options = {
    'page-size': 'A4',
    'margin-top': '1in',        # Margem superior de 1 polegada
    'margin-right': '1in',      # Margem direita de 1 polegada
    'margin-bottom': '1in',     # Margem inferior de 1 polegada
    'margin-left': '1in',       # Margem esquerda de 1 polegada
    'encoding': "latin1",        # Codificação para suportar caracteres especiais
    'no-outline': None,         # Remove o outline (contorno)
    '--enable-local-file-access': None  # Permite o acesso a arquivos locais
}

for filename in os.listdir(input_folder):
    if filename.endswith('.html') or filename.endswith('.htm'):
        # Caminho completo para o arquivo HTML ou HTM
        input_html = os.path.join(input_folder, filename)
        
        # Caminho completo para o arquivo PDF de saída
        output_pdf = os.path.join(output_folder, filename.replace('.html', '.pdf').replace('.htm', '.pdf'))
        
        # Verifique se o arquivo PDF já existe
        if not os.path.exists(output_pdf):
            # Converte o arquivo HTML ou HTM em PDF com as opções especificadas e configuração do caminho do wkhtmltopdf
            pdfkit.from_file(input_html, output_pdf, options=options, configuration=config)
            print(f'Arquivo PDF gerado com sucesso: {output_pdf}')
        else:
            print(f'O arquivo PDF já existe: {output_pdf}')
