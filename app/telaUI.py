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
            [sg.Text("Area resultados: Paragrafo e Links", size=(40, 1), justification='center', font=('Helvetica', 12, 'bold'))],
            [sg.Multiline(size=(40, 10), key="-RESULTADO-", expand_x=True, expand_y=True, default_text= self.CarregarParagrafosIdentificados())],
            [sg.Text("", size=(40, 1))],  # Margem superior entre a Multiline e o botão "Relatório PDF"
            [
                sg.Button(f"Quantidade de links: {self.quantLinks}", font=('Helvetica', 12, 'bold'), key='-INCREMENTELINKS-'),
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
                self.IdentificarESalvarParagrafos(conteudo)
                conteudo_paragrafos = self.CarregarParagrafosIdentificados()
                self.window["-RESULTADO-"].update(conteudo_paragrafos)
                sg.popup("Conteúdo salvo com sucesso!")

            elif event == "-INCREMENTELINKS-":
                self.quantLinks += 1
                self.window['-INCREMENTELINKS-'].update(f'Quantidade de links: {self.quantLinks}' )

            elif event == "Relatório PDF":
                self.SalvarPDF()
                sg.popup("PDF salvo com sucesso!", title="Salvar PDF")
    
            
        self.window.close()
