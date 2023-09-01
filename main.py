import os
from app.loop import Loop
# from app.file import File
# from app.similar import Similar


if __name__ == "__main__":

    # fileInput         = 'entrada.txt'
    # fileMonitoring    = 'monitoramento.txt'
    # fileReportTXT     = 'relatorio.txt' 

    dir  = 'file_text_test'

    fileInput           = os.path.join(dir, 'entrada.txt')
    fileMonitoring      = os.path.join(dir, 'monitoramento.txt')
    fileSavedParagraphs = os.path.join(dir, 'paragrafos.txt')
    fileReportTXT       = os.path.join(dir, 'relatorio.txt')
    time     = 10 

    

    loop = Loop(fileInput, fileMonitoring, fileReportTXT, fileSavedParagraphs, time)
    loop.mainLoop()

    # file    = File(fileMonitoring)
    # similar = Similar()

    # if file.CompareFiles(fileInput, fileMonitoring) == 0:
    #     contents = file.ReadFile(fileInput)
    #     file.WriteFile(contents, fileMonitoring)

    #     paragraphs = file.IdentifyParagraphs(contents)

    #     for paragraph in paragraphs:
    #         links = similar.LinksSimilar(paragraph)
    #         file.SaveParagraphsToFile(fileReportTXT, paragraph, links)
            