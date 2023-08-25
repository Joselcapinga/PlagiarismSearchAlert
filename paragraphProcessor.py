import searchParagraph

class ParagraphProcessor(searchParagraph.SearchParagraph):
    
    inputFile  = ""
    outputFile = ""
    
    #O construtor da classe. Recebe os caminhos dos arquivos de entrda e saida
    def __init__(self, inputFile, outputFile):
        self.inputFile  = inputFile
        self.outputFile = outputFile
    
    #Método para ler o contúdo do arquivo de entrada.
    def ReadInputFile(self):
        with open(self.inputFile, 'r') as intput_file:
            content = intput_file.read()
            return content

    #Método para escrever o conteúdo em um arquivo de saída 
    def WriteOutFile(self, content):
        with open(self.outputFile, 'w') as out_file:
             out_file.write(content)

    #Método para 
    def ProcessParagraphs(self, input_content):
        sentences = []
        paragraph = ""

        for char in input_content: 
            paragraph += char
            if char in ['.', '!', '?']:
                sentences.append(paragraph)
                paragraph = ""
        
        if sentences:
            
            new_paragraph = []

            for sentence in sentences:
                similar_paragraph = self.search_paragraph(sentence)
                new_paragraph.append(sentence + "\n" + similar_paragraph)
            
            new_paragraph = "\n".join(sentences)
            self.WriteOutFile(new_paragraph)
            print("Parágrafo identificado e copiado para arquivo de saida.")