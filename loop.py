import paragraphProcessor
import time

class Loop(paragraphProcessor.ParagraphProcessor):
    
    def __init__(self, inputFile, outputFile):
        super().__init__(inputFile, outputFile) 

    def mainLoop(self):
        try:
            while True:
                input_content = self.ReadInputFile()
                self.ProcessParagraphs(input_content)
                # Espera por 30 segundos
                time.sleep(30)  
        except:
            print("Programa encerrado pelo usuário.")
