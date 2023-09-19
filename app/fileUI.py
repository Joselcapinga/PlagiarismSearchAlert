# import time
# import re
import os
from googlesearch import search
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak
from reportlab.lib.enums import TA_CENTER


class FileUI:

    def __init__(self):

        dir  = 'file_text_test'
        
        self.fileMonitoramento = os.path.join(dir,"monitoramento.txt")
        self.fileParagrafos    = os.path.join(dir,"paragrafo_identificados.txt")
        self.relatorioPDF      = os.path.join(dir,"relatorio.pdf")

        self.CriarArquivos()
 

    def CriarArquivos(self):
        
        import os
        if not os.path.exists(self.fileMonitoramento):
            with open(self.fileMonitoramento, "w") as fileInput:
                pass
        if not os.path.exists(self.fileParagrafos):
            with open(self.fileParagrafos, "w") as fileInput:
                pass

    # Função para salvar o conteúdo da ScrolledText em um arquivo 'monitoramento.txt'
    def SalvarConteudo(self, conteudo):
        with open(self.fileMonitoramento, "r") as arquivo:
            conteudo_anterior = arquivo.read()

        if conteudo != conteudo_anterior:
            with open(self.fileMonitoramento, "w") as arquivo:
                arquivo.write(conteudo)


    # Função para identificar e salvar parágrafos em 'paragrafo_identificados.txt' com links de pesquisa do Google
    def IdentificarESalvarParagrafos(self, conteudo, numLinks):
        # Utilize uma expressão regular para dividir o conteúdo em parágrafos
        # paragrafos = re.split(r'(?<=[.!?])\s+', conteudo)

        delimitadores_sentecas = ['.', '!', '?']
        sentencas = []
        current_sentence = ''
        paragrafos = []
        
        for char in conteudo:
                current_sentence += char
                if char in delimitadores_sentecas:
                    sentencas.append(current_sentence.strip())
                    current_sentence = ''


        # permito só paragrafo
        paragrafos = [sentence for sentence in sentencas if any(sentence.endswith(delimitador) for delimitador in delimitadores_sentecas)]


        # Crie o arquivo 'paragrafo_identificados.txt' se ele não existir
        if not os.path.exists(self.fileParagrafos):
            open(self.fileParagrafos, "a").close()

        # Verifique se o parágrafo não existe antes de salvar em 'paragrafo_identificados.txt'
        paragrafos_existentes = set()
        with open(self.fileParagrafos, "r") as arquivo:
            for linha in arquivo:
                paragrafos_existentes.add(linha.strip())

        with open(self.fileParagrafos, "a") as arquivo:
            for paragrafo in paragrafos:
                if paragrafo not in paragrafos_existentes:
                    arquivo.write(paragrafo + "\n\n")

                    # Realize a pesquisa no Google e salve os links de retorno
                    # links = []
                    # for resultado in search(paragrafo, num=5, stop=5, pause=2):
                    #     links.append(resultado)
                    arquivo.write("\nLinks de pesquisa do Google:\n")
                    arquivo.write("\n".join(self.LinksSimilar(paragrafo, numLinks)) + "\n\n")

                    paragrafos_existentes.add(paragrafo)


    # Função para carregar o conteúdo do arquivo 'monitoramento.txt' na área de texto
    def CarregarConteudo(self):
        try:
            with open(self.fileMonitoramento, "r") as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            return ""


    # Função para carregar o conteúdo do arquivo 'paragrafo_identificados.txt' na segunda área de texto
    def CarregarParagrafosIdentificados(self):
        try:
            with open(self.fileParagrafos, "r") as arquivo:
                return arquivo.read()
        except FileNotFoundError:
            return ""


    # Função para criar 'paragrafo_identificados.txt' se ele não existir
    def CriarParagrafoIdentificados(self):
        if not os.path.exists(self.fileParagrafos):
            open(self.fileParagrafos, "a").close()


    # Função para salvar o conteúdo em PDF com formatação
    def SalvarPDF(self):
        conteudo_paragrafos = self.CarregarParagrafosIdentificados()

        if conteudo_paragrafos:
            # Crie um arquivo PDF com o conteúdo formatado
            doc = SimpleDocTemplate(self.relatorioPDF, pagesize=letter)
            styles = getSampleStyleSheet()

            # Crie um Paragraph personalizado com alinhamento centralizado
            cabecalho = Paragraph("<center>Relatório</center>", styles["Heading1"])
            conteudo = [cabecalho]

            # Adicione o conteúdo dos parágrafos com quebras de linha
            paragrafos = conteudo_paragrafos.split("\n\n")
            for paragrafo in paragrafos:
                p = Paragraph(paragrafo, styles["Normal"])
                conteudo.append(p)
                conteudo.append(Spacer(1, 12))  # Espaço entre os parágrafos

            # Construa o arquivo PDF
            doc.build(conteudo)
            # sg.popup("PDF salvo com sucesso!", title="Salvar PDF")
