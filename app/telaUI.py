import PySimpleGUI as sg
import threading
import time
import app.fileUI as fileUI



class TelaUI(fileUI.FileUI):

    def __init__(self):
              
        super().__init__()

        sg.theme('LightGreen')
        sg.set_options(element_padding=(0, 0))

        menu = [
            ['&File', ['&Salvar o conteúdo', '&Relatório PDF', '&Sair']]
        ]

        #criação do layout
        layout = [
            [sg.Menu(menu, tearoff=True, font=('Helvetica', 12), key='-MENUBAR-')],
            [sg.Text("Area de Editar", size=(40, 1), justification='center', font=('Helvetica', 12, 'bold'))],
            [sg.Multiline(size=(40, 10), key="-EDITAR-", expand_x=True, expand_y=True, default_text= self.CarregarConteudo())],
            [sg.Text("", size=(40, 1))],
            [sg.Button("Salvar o conteúdo", font=('Helvetica', 12, 'bold'))],
            [sg.Text("", size=(40, 1))],
            [sg.Text("Area resultados: Paragrafo e Links", size=(40, 1), justification='center', font=('Helvetica', 12, 'bold'))],
            [sg.Multiline(size=(40, 10), key="-RESULTADO-", expand_x=True, expand_y=True, default_text= self.CarregarParagrafosIdentificados())],
            [sg.Text("", size=(40, 1))],  # Margem superior entre a Multiline e o botão "Relatório PDF"
            [sg.Button("Relatório PDF", font=('Helvetica', 12, 'bold')), sg.Button("Sair", font=('Helvetica', 12, 'bold'))]  # Botões na mesma linha
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
            time.sleep(30)
            conteudo = self.window["-EDITAR-"].get()
            self.SalvarConteudo(conteudo)
            self.IdentificarESalvarParagrafos(conteudo)
            conteudo_paragrafo = self.CarregarParagrafosIdentificados()
            self.window["-RESULTADO-"].update(conteudo_paragrafo)


    def LoopUI(self):

        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, "Sair"):
                break

            elif event == "Salvar o conteúdo":

                conteudo = values["-EDITAR-"]
                self.SalvarConteudo(conteudo)
                self.IdentificarESalvarParagrafos(conteudo)
                conteudo_paragrafos = self.CarregarParagrafosIdentificados()
                self.window["-RESULTADO-"].update(conteudo_paragrafos)
                sg.popup("Conteúdo salvo com sucesso!")

            elif event == "Relatório PDF":
                self.SalvarPDF()
                sg.popup("PDF salvo com sucesso!", title="Salvar PDF")
    
            
        self.window.close()
