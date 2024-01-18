# converte arquivos em pdf
import os
import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas

# Criar a classe que representa a interface gráfica do programa
class FileToPdfConverterApp:
    def __init__(self, root):
        # Configurar a janela principal com o título "File to PDF Converter" e cor de fundo preta
        self.root = root
        self.root.title("File to PDF Converter")
        self.root.configure(background="black")
        
        # Inicializar uma lista para guardar os caminhos dos arquivos selecionados
        self.file_paths = []

        # Criar um campo para guardar o caminho da pasta de destino (onde os arquivos PDF serão salvos)
        self.output_folder = tk.StringVar()

        # Chamar a função para criar os elementos da interface
        self.create_widgets()

    # Função para criar os elementos da interface gráfica
    def create_widgets(self):
        # Botão para selecionar os arquivos
        btn_select = tk.Button(self.root, text="Selecionar Arquivos", command=self.select_files)
        btn_select.pack(pady=10)

        # Campo para exibir o caminho da pasta de destino selecionada
        output_label = tk.Label(self.root, text="Pasta de destino selecionada:", foreground="blue", background="black")
        output_label.pack()
        output_entry = tk.Entry(self.root, textvariable=self.output_folder)
        output_entry.pack()

        # Botão para selecionar a pasta de destino
        btn_output = tk.Button(self.root, text="Selecionar Pasta de Destino", command=self.choose_output_folder)
        btn_output.pack(pady=10)

        # Botão para converter os arquivos em PDF
        btn_convert = tk.Button(self.root, text="Converter para PDF", command=self.convert_to_pdf)
        btn_convert.pack(pady=10)

    # Função para abrir a janela de seleção de arquivos e guardar os caminhos dos arquivos selecionados
    def select_files(self):
        # Abrir a janela de seleção de arquivos
        file_paths = filedialog.askopenfilenames()
        # Guardar os caminhos dos arquivos selecionados na lista
        self.file_paths.extend(file_paths)

    # Função para abrir a janela de seleção de pasta e guardar o caminho da pasta de destino
    def choose_output_folder(self):
        # Abrir a janela de seleção de pasta
        output_folder = filedialog.askdirectory()
        # Guardar o caminho da pasta de destino
        self.output_folder.set(output_folder)

    # Função para converter os arquivos selecionados em PDF
    def convert_to_pdf(self):
        try:
            # Obter o caminho da pasta de destino
            output_folder = self.output_folder.get()
            # Verificar se a pasta de destino existe
            if not os.path.isdir(output_folder):
                raise FileNotFoundError("A pasta de destino selecionada não foi encontrada.")

            # Loop para converter cada arquivo selecionado em PDF
            for file_path in self.file_paths:
                # Verificar se o arquivo existe
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f"O arquivo '{file_path}' não foi encontrado.")

                # Obter o nome do arquivo sem extensão
                file_name, file_extension = os.path.splitext(os.path.basename(file_path))

                # Criar o caminho para o arquivo PDF, com o mesmo nome do arquivo original e a extensão ".pdf"
                pdf_path = os.path.join(output_folder, f"{file_name}.pdf")

                # Iniciar um PDF
                c = canvas.Canvas(pdf_path)
                c.setFont("Helvetica", 12)

                # Abrir o arquivo original e ler o conteúdo
                with open(file_path, "rb") as file:
                    content = file.read()

                    # Escrever o conteúdo do arquivo original no PDF
                    c.drawString(50, 800, content.decode("utf-8"))

                # Salvar o PDF
                c.save()

            # Exibir mensagem de sucesso
            self.show_info("Sucesso!", "Arquivos convertidos para PDF com sucesso.")
        except Exception as e:
            # Exibir mensagem de erro 
            self.show_info("Erro!", str(e))

    # Função para exibir uma janela de mensagem informativa
    def show_info(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)
        popup.configure(background="black")
        tk.Label(popup, text=message, foreground="blue", background="black").pack()
        tk.Button(popup, text="OK", command=popup.destroy).pack()

# Função principal 
if __name__ == "__main__":
    root = tk.Tk() # Criar a janela principal
    root.configure(background="black") # Definir o fundo da janela como preto
    app = FileToPdfConverterApp(root) # Criar a instância da interface gráfica
    root.mainloop() # Iniciar o loop principal da interface
