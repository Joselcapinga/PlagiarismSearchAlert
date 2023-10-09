from flask import Flask, request, jsonify
import os
import requests
from bs4 import BeautifulSoup
import fitz

app = Flask(__name__)

@app.route('/processar_link', methods=['POST'])
def processar_link():
    link = request.json.get('link')
    query_original = request.json.get('query')

    # Remove ".", "?", ou "!" do final da query e converte para minúsculas
    query = query_original.rstrip('.?!').lower()

    encontrado = False

    if link.endswith('.pdf'):
        # Processa PDF
        texto_pdf = extrair_texto_pdf(link).lower()
        if query in texto_pdf:
            encontrado = True
    else:
        # Processa HTML
        try:
            conteudo_html = extrair_conteudo_html(link).lower()
            if query in conteudo_html:
                encontrado = True
        except Exception as e:
            print(f"Erro ao obter conteúdo HTML: {str(e)}")

    if encontrado:
        return jsonify({"status": "Sucesso", "mensagem": encontrado}), 200
    else:
        return jsonify({"status": "Sucesso", "mensagem": encontrado}), 200


def extrair_texto_pdf(link):
    # Baixa o PDF
    pdf_path = 'temp.pdf'
    response = requests.get(link)
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(response.content)
    
    # Extrai o texto do PDF e remove quebras de linha
    pdf_document = fitz.open(pdf_path)
    texto_pdf = ''
    for page in pdf_document:
        texto_pdf += page.get_text().replace('\n', ' ')
    
    # Exclui o arquivo temporário
    os.remove(pdf_path)

    return texto_pdf

def extrair_conteudo_html(link):
    # Faz a requisição para obter o conteúdo HTML
    response = requests.get(link)
    response.raise_for_status()  # Levanta uma exceção se a requisição falhar
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Obtém apenas o texto e remove quebras de linha
    conteudo_html = soup.get_text().replace('\n', ' ')
    
    # Salva o conteúdo em um arquivo
    with open('conteudo.txt', 'w', encoding='utf-8') as file:
        file.write(conteudo_html)
    
    return conteudo_html

if __name__ == '__main__':
    app.run(debug=True, port=8080)
