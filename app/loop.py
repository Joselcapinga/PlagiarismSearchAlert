import os
import time
import app.file as file
import app.similar as similar

class Loop(file.File, similar.Similar):

    fileOut    = None # arquivo de entrada
    timeVerif  = None # tempo de verificação
    
    def __init__(self, file_out, timeVerif):

        self.fileOut  = file_out

        if timeVerif != None or timeVerif == 0:
            self.timeVerif = timeVerif
        else:
            self.timeVerif = 10
    
    def mainLoop(self):
        
        last_position = 0
        while True:
            try:
                new_lines, last_position = self.ReadNewlines(self.fileOut,last_position)
                if new_lines:
                    for line in new_lines:
                        print(f"Nova frase encontrada: {line}")
                        results = self.LinksSimilar(line)
                        if results:
                            print("Resultados de pesquisas: ")
                            for result in results:
                                print(f"URL: {result}")
                        else:
                            print("Nenhum resultado encontrado.")
            except FileNotFoundError:
                print(f"Arquivo não encontrado. Verifique o nome do arquivo")
            except Exception as e:
                print("Ocorreu um erro: ", e)

            # verifica a cada 10 segundos
            time.sleep(self.timeVerif)