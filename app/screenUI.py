import PySimpleGUI as sg
import threading
import time
import datetime
import app.file as file
import app.similar as similar


class ScreenUI(file.File, similar.Similar):

    def __init__(self):
              
        super().__init__()

        self.quantLinks     = 4 
        self.statusResult   = True 
        self.tempoChecagem  = 20    
        ano_atual = datetime.datetime.now().year

        sg.theme('LightGreen')
        sg.set_options(element_padding=(0, 0))

        menu = [
            ['&File', ['&Salvar o conteúdo', '&Relatório PDF','&Exportar .doc', '&Sair X']],
            ['&Ajudas', ['&Manual de usabilidade da ferramenta']],
            ['&Sobre', ['&Sobre a Plagiarism Search Alert']],
        ]

        #criação do layout
        layout = [
            [sg.Menu(menu, tearoff=True, font=('Helvetica', 12), key='-MENUBAR-')],
            [sg.Text("Area de Editar", size=(40, 1), justification='center', font=('Helvetica', 12, 'bold'))],
            [sg.Multiline(size=(40, 10), key="-EDITAR-", expand_x=True, expand_y=True, default_text= self.CarregarConteudo(1))],
            [sg.Text("", size=(40, 1))],
            [
                sg.Button("Salvar o conteúdo", font=('Helvetica', 12, 'bold')),
                sg.Button("Exportar .doc", font=('Helvetica', 12, 'bold'))
            
            ],
            [sg.Text("", size=(40, 1))],
            [
                [sg.Text("Paragrafo e conteúdos semelhantes", justification='center', font=('Helvetica', 12, 'bold'))],
            ],
            [
                # encontrei mais textos similiares, verifica os links na area de resultados. Colocar em cor vermelha ao lado da quantidade de links atuais
            ],
            [sg.Multiline(size=(40, 10), key="-RESULTADO-", expand_x=True, expand_y=True, disabled=True, default_text= self.CarregarConteudo(2))],
            [sg.Text("", size=(40, 1))],  # Margem superior entre a Multiline e o botão "Relatório PDF"
            [
                sg.Button("Status Paragrafos e consulta no banco de textos: Ativo", font=('Helvetica', 12, 'bold'), key='-StusResultado-'), 
                sg.Button("Relatório PDF", font=('Helvetica', 12, 'bold')), 
                sg.Button("Sair X", font=('Helvetica', 12, 'bold')),
             ],  # Botões na mesma linha

                [sg.Text("", size=(40, 1))],  # Adicionar espaço vertical aqui
                [sg.Text(f"Plagiarism Search Alert @ {ano_atual}. Versão 1.0.0 ",size=(40, 1), justification='center')],

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

            time.sleep(self.tempoChecagem)
            conteudo = self.window["-EDITAR-"].get()
            self.SalvarConteudo(conteudo)
            self.IdentificarESalvarParagrafos(conteudo)
            if self.statusResult == True:
                conteudo_paragrafo = self.CarregarConteudo(2)
                self.window["-RESULTADO-"].update(conteudo_paragrafo)

    # Função para exibir a caixa de diálogo de ajuda
    def AjudassMenu(self):
        
        sg.popup("Aqui estão as instruções de ajuda:",
                "1. Area de Editar: Area de editar o texto que será consultado a semeliaridade de textos no google search.",
                "2. Botão Salvar o conteúdo: Salva o contúdo da area de Editar",
                "3. Botão Exportar .doc: exporta docx do conteúdo da area de edição",
                "5. Botão 'Relatório PDF' exporta um relatório do conteúdo da area Paragrafos, Links no formato PDF.",
                "6. Botão 'Sair X' para fechar o programa.",
                "7. Botão 'Status Paragrafos e consulta no banco de textos' ativa e desativa a consulta no banco de textos.",
                title="Instruções de Ajuda"
                )
        
    def Sobre(self):
        
        sg.popup("Sbre:",
                "Nome da Ferramenta: Plagiarism Search Alert",
                "Autor: José Lohame Capinga",
                "Orientador: Prof. Dr. João Paulo Aires",
                "Universidade Tecnológica Federal do Paraná (UTFPR) - Campus Ponta Grossa",
                "Trabalho de Conclusão de Curso - Bacharelado em Ciência da Computação.",
                "",
                title="Sobre a Sobre a Plagiarism Search Alert"
                )


    def LoopUI(self):

        while True:

            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, "Sair X"):
                break
            elif event == "Salvar o conteúdo":
                conteudo = values["-EDITAR-"]
                self.SalvarConteudo(conteudo)
                self.IdentificarESalvarParagrafos(conteudo)
                conteudo_paragrafos = self.CarregarConteudo(2)
                self.window["-RESULTADO-"].update(conteudo_paragrafos)
                sg.popup("Conteúdo salvo com sucesso!")
            elif event == "-StusResultado-":
                if self.statusResult == True:
                    self.statusResult = False
                    self.window['-StusResultado-'].update('Status Paragrafos e consulta no banco de textos: Desativo')
                else:
                    self.statusResult = True
                    self.window['-StusResultado-'].update(f'Status Paragrafos e consulta no banco de textos: Ativo')
            elif event == "Relatório PDF":
                self.SalvarPDF()
                sg.popup("PDF salvo com sucesso!", title="Salvar PDF")

            elif event == "Manual de usabilidade da ferramenta":
                self.AjudassMenu()
            
            elif event == "Sobre a Plagiarism Search Alert":
                self.Sobre()

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
