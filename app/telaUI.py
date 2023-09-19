import PySimpleGUI as sg
import threading
import time
import app.fileUI as fileUI
import app.similar as similar


class TelaUI(fileUI.FileUI, similar.Similar):

    def __init__(self):
              
        super().__init__()

        # quantidade de links na consulta do google search
        self.quantLinks = 4

        sg.theme('LightGreen')
        sg.set_options(element_padding=(0, 0))

        menu = [
            ['&Configurações', ['Manual de usabilidade da ferramenta']],
            ['&File', ['&Salvar o conteúdo', '&Relatório PDF', '&Sair X']],
            ['&Help', ['Manual de usabilidade da ferramenta']]
        ]

        #criação do layout
        layout = [
            [sg.Menu(menu, tearoff=True, font=('Helvetica', 12), key='-MENUBAR-')],
            [sg.Text("Area de Editar", size=(40, 1), justification='center', font=('Helvetica', 12, 'bold'))],
            [sg.Multiline(size=(40, 10), key="-EDITAR-", expand_x=True, expand_y=True, default_text= self.CarregarConteudo())],
            [sg.Text("", size=(40, 1))],
            [
                sg.Button("Salvar o conteúdo", font=('Helvetica', 12, 'bold')),
                sg.Button("Exportar .doc", font=('Helvetica', 12, 'bold'))
            
            ],
            [sg.Text("", size=(40, 1))],
            [
                [sg.Text("Paragrafo, Links com conteúdos semelhantes", justification='center', font=('Helvetica', 12, 'bold'))],
                #  sg.Text(str(self.quantLinks), size=(40, 1), justification='center', font=('Helvetica', 12, 'bold'), key='-QUANTIDADELINKS-')],
                [sg.Text("Quantidade de links atual:", font=('Helvetica', 12, 'bold')),
                sg.Text(str(self.quantLinks), size=(40, 1), justification='center', font=('Helvetica', 12, 'bold'), key='-QUANTIDADELINKS-')]

            ],
            [
                
            ],
            [sg.Multiline(size=(40, 10), key="-RESULTADO-", expand_x=True, expand_y=True, default_text= self.CarregarParagrafosIdentificados())],
            [sg.Text("", size=(40, 1))],  # Margem superior entre a Multiline e o botão "Relatório PDF"
            [
                sg.Button("+ links", font=('Helvetica', 12, 'bold'), key='-INCREMENTELINKS-'),
                sg.Button("- links", font=('Helvetica', 12, 'bold'), key='-DECREMENTELINKS-'),
                sg.Button("Relatório PDF", font=('Helvetica', 12, 'bold')), 
                sg.Button("Sair X", font=('Helvetica', 12, 'bold')),
                
             ]  # Botões na mesma linha
        ]

        # configuração dos elementos da tela
        self.window = sg.Window("Plagiarism Search Alert", layout,
                           default_element_size=(12, 1),
                           default_button_element_size=(12, 1),
                           finalize=True,
                           resizable=True
                           )
        
        thread = threading.Thread(target= self.SalvaAutomaticamente)
        thread.daemon = True
        thread.start()

        #executa a tela
        self.LoopUI()


    def SalvaAutomaticamente(self):

        while True:
            time.sleep(15)
            conteudo = self.window["-EDITAR-"].get()
            self.SalvarConteudo(conteudo)
            self.IdentificarESalvarParagrafos(conteudo, self.quantLinks)
            conteudo_paragrafo = self.CarregarParagrafosIdentificados()
            self.window["-RESULTADO-"].update(conteudo_paragrafo)


    def LoopUI(self):

        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, "Sair X"):
                break

            elif event == "Salvar o conteúdo":
                conteudo = values["-EDITAR-"]
                self.SalvarConteudo(conteudo)
                self.IdentificarESalvarParagrafos(conteudo, self.quantLinks)
                conteudo_paragrafos = self.CarregarParagrafosIdentificados()
                self.window["-RESULTADO-"].update(conteudo_paragrafos)
                sg.popup("Conteúdo salvo com sucesso!")

            elif event == "-INCREMENTELINKS-" and self.quantLinks < 10:
                self.quantLinks += 1
                self.window['-QUANTIDADELINKS-'].update(str(self.quantLinks))
            
            elif event == "-DECREMENTELINKS-" and self.quantLinks > 3:
                self.quantLinks -= 1
                self.window['-QUANTIDADELINKS-'].update(str(self.quantLinks))

            elif event == "Relatório PDF":
                self.SalvarPDF()
                sg.popup("PDF salvo com sucesso!", title="Salvar PDF")

            elif event == "Exportar .doc":
                conteudo = values["-EDITAR-"]

                if conteudo:
                    self.SalvarDoc(conteudo)
                    if self.SalvarDoc(conteudo) == 1:
                        sg.popup('Conteúdo exportado sucesso para "document_exportado.docx"')
                    else:
                        sg.popup('Erro ao exportar conteúdo para "document_exportado.docx"')
                else:
                    sg.popup('Não existe conteúdo para exportar no "document_exportado.docx"')
        
        
        self.window.close()
