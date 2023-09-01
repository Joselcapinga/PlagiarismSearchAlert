import time
import app.file as file
import app.similar as similar

class Loop(file.File, similar.Similar):
    
    def __init__(self, fileInput, fileMonitoring, fileReportTXT, fileSavedParagraphs, timeVerif):

        self.fileInput              = fileInput
        self.fileMonitoring         = fileMonitoring
        self.fileReportTXT          = fileReportTXT
        self.fileSavedParagraphs    = fileSavedParagraphs

        self.create(self.fileMonitoring, self.fileSavedParagraphs)

        if timeVerif != None or timeVerif == 0:
            self.timeVerif = timeVerif
        else:
            self.timeVerif = 30
    
    def mainLoop(self):
        while True:
            try:
                if self.CompareFiles(self.fileInput, self.fileMonitoring) == 0:
                    
                    contents = self.ReadFile(self.fileInput)
                    # self.WriteFile(contents, self.fileMonitoring)
                    report   = self.ReadFile(self.fileReportTXT)

                    paragraphs       = self.IdentifyParagraphs(contents)                    

                    for paragraph in paragraphs:
                        if paragraph not in report:
                            links = self.LinksSimilar(paragraph)
                            self.SaveParagraphsToFile(self.fileReportTXT, paragraph, links)
                            self.SaveParagraphsToFile(self.fileSavedParagraphs, paragraph)
            except FileNotFoundError:
                print(f"Arquivo não encontrado. Verifique o nome do arquivo")
            except Exception as e:
                print("Ocorreu um erro: ", e)

            # verifica a cada 10 segundos
            time.sleep(self.timeVerif)