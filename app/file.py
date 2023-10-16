import os
from googlesearch import search
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak
from reportlab.lib.enums import TA_CENTER
import docx


class File:

    def __init__(self):

        dir  = 'file_salve'
        
        self.fileMonitoramento   = os.path.join(dir,"monitoramento.txt")
        self.fileParagrafos      = os.path.join(dir,"paragrafo_identificados.txt")
        self.relatorioPDF        = os.path.join(dir,"relatorio.pdf")
        self.fileBanco           = os.path.join(dir,"banco_de_textos.txt")
        self.conteudoBanco       = '' 

        self.CriarArquivos()
        self.CarregaBanco()


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

    # Função para carregar o conteúdo do arquivo 'monitoramento.txt' na área de texto
    def CarregarConteudo(self, opc):
        try:
            if opc == 1:
                with open(self.fileMonitoramento, "r") as arquivo:
                    return arquivo.read()
            elif opc == 2:
                 with open(self.fileParagrafos, "r") as arquivo:
                    return arquivo.read()

        except FileNotFoundError:
            return ""

    # Função para identificar e salvar parágrafos em 'paragrafo_identificados.txt' com links de pesquisa do Google
    def IdentificarESalvarParagrafos(self, conteudo):

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
        paragrafos = [sentence 
                      for sentence in sentencas 
                        if any(sentence.endswith(delimitador) 
                            for delimitador in delimitadores_sentecas)]

        # Verifique se o parágrafo não existe antes de salvar em 'paragrafo_identificados.txt'
        paragrafos_existentes = set()
        with open(self.fileParagrafos, "r") as arquivo:
            for linha in arquivo:
                paragrafos_existentes.add(linha.strip())

        with open(self.fileParagrafos, "a") as arquivo:
            for paragrafo in paragrafos:
                if paragrafo not in paragrafos_existentes:
                    arquivo.write(paragrafo + "\n\n")

                    paragraf = paragrafo.lower()
                    # Remove "." , "?", ou "!" do final do paragrafo
                    paragraf = paragraf.rstrip('.?!')

                    paragrafos_similiares = self.ConsultaParagrafo(paragraf)

                    if len(paragrafos_similiares) > 0:
                        arquivo.write("Similaridades encontradas no banco de dados: " + "\n\n")
                        arquivo.write("\n".join(paragrafos_similiares)+"\n")
                        arquivo.write(self.Jaccard(paragraf, paragrafos_similiares))
                        arquivo.write("\n"+("*"*100)+"\n\n")
                    else:
                        arquivo.write("O parágrafo não existe similaridade no banco de dados" + "\n\n")
                        arquivo.write("\n"+("*"*100)+"\n\n")
                    paragrafos_existentes.add(paragrafo)

    # Função para salvar o conteúdo em PDF com formatação
    def SalvarPDF(self):
        try:
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
                return True
        except:
            return False


    def SalvarDoc(self, conteudo):
        try:
            doc = docx.Document()
            doc.add_paragraph(conteudo)
            doc.save('document_exportado.docx')
            return True
        except:
            return False


    def ConsultaParagrafo(self, paragrafo):
        
        # dividindo em palavras a frase
        palavras_a_verificar = paragrafo.split()
        palavras_no_arquivo  = []
        partesEncontradas    = []

        # verificando se cada palavra existe no arquivo
        for palavra in palavras_a_verificar:
            if palavra in self.conteudoBanco:
                palavras_no_arquivo.append(palavra)

        # verifcando a parte achada
        encontrado          = ""
        for palavra_no_arquivo in palavras_no_arquivo:

            encontrado+= palavra_no_arquivo
    
            if encontrado not in self.conteudoBanco:
                new_str  = encontrado.replace(palavra_no_arquivo, '')
                if len(encontrado) > 10:
                    partesEncontradas.append(new_str)

                encontrado = ""
            else:
                encontrado+= " "
        
        if len(encontrado) > 10:
            partesEncontradas.append(encontrado)
    
        return partesEncontradas

    def CarregaBanco(self):
        with open(self.fileBanco, 'r') as arquivo:
            self.conteudoBanco = arquivo.read().lower()
