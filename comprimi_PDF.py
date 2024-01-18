# comprimi pdf
import os
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter

# Criar a classe que representa a interface gráfica do programa
class PDFCompressorApp:
    def __init__(self, root):
        # Configurar a janela principal com o título "PDF Compressor" e cor de fundo preta
        self.root = root
        self.root.title("PDF Compressor")
        self.root.configure(background="black")
        
        # Inicializar as variáveis para guardar os caminhos dos arquivos, pasta de saída e tamanho desejado
        self.file_paths = [] # Guardará os caminhos dos PDFs selecionados
        self.output_folder = tk.StringVar() # Guardará o caminho da pasta de saída
        self.target_size = tk.StringVar() # Guardará o tamanho desejado para os PDFs

        # Chamar a função para criar os elementos da interface
        self.create_widgets()

    # Função para criar os elementos da interface gráfica
    def create_widgets(self):
        # Botão para selecionar os PDFs
        btn_select = tk.Button(self.root, text="Selecionar PDFs", command=self.select_files)
        btn_select.pack(pady=10)

        # Botão para selecionar a pasta de saída
        btn_output = tk.Button(self.root, text="Selecionar Pasta de Saída", command=self.choose_output_folder)
        btn_output.pack(pady=10)

        # Campo para inserir o tamanho desejado (em KB)
        label_target_size = tk.Label(self.root, text="Tamanho desejado (KB):", foreground="blue", background="black")
        label_target_size.pack()
        entry_target_size = tk.Entry(self.root, textvariable=self.target_size)
        entry_target_size.pack()

        # Botão para iniciar a compressão
        btn_compress = tk.Button(self.root, text="Comprimir PDFs", command=self.compress_pdfs)
        btn_compress.pack(pady=20)

    # Função para abrir a janela de seleção de arquivos e guardar os caminhos dos PDFs selecionados
    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Arquivos PDF", "*.pdf")])
        self.file_paths.extend(file_paths)

    # Função para abrir a janela de seleção de pasta e guardar o caminho da pasta de saída
    def choose_output_folder(self):
        self.output_folder.set(filedialog.askdirectory())

    # Função para comprimir os PDFs com base no tamanho desejado
    def compress_pdfs(self):
        try:
            # Pegar o caminho da pasta de saída e o tamanho desejado em KB do usuário
            output_folder = self.output_folder.get()
            target_size_kb = int(self.target_size.get())
            target_size_bytes = target_size_kb * 1024 # Converter o tamanho para bytes

            # Verificar se a pasta de saída existe
            if not os.path.isdir(output_folder):
                raise FileNotFoundError("O diretório de saída selecionado não foi encontrado.")

            # Loop para comprimir cada PDF selecionado
            for file_path in self.file_paths:
                # Verificar se o arquivo PDF existe
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f"O arquivo PDF '{file_path}' não foi encontrado.")

                # Definir o caminho do arquivo comprimido
                output_file = os.path.join(output_folder, f"compressed_{os.path.basename(file_path)}")

                # Abrir o PDF original para leitura (modo "rb" significa leitura binária)
                with open(file_path, "rb") as pdf_file:
                    # Criar leitor do PDF original e escritor para o PDF comprimido
                    pdf_reader = PdfFileReader(pdf_file)
                    pdf_writer = PdfFileWriter()

                    # Copiar todas as páginas do PDF original para o PDF comprimido
                    for page_num in range(pdf_reader.getNumPages()):
                        page = pdf_reader.getPage(page_num)
                        pdf_writer.addPage(page)

                    # Definir a qualidade de compressão (0 para máxima, 9 para mínima)
                    pdf_writer.setCompression(9)

                    # Escrever o PDF comprimido no arquivo de saída
                    pdf_writer.write(output_file)
                
                # Obter o tamanho do PDF original e do PDF comprimido
                original_size = os.path.getsize(file_path)
                compressed_size = os.path.getsize(output_file)
                
                # Se o PDF comprimido for menor ou igual ao tamanho desejado, remover o arquivo temporário criado
                if compressed_size <= target_size_bytes:
                    os.remove(output_file)
                else:
                    # Se o tamanho do PDF comprimido for maior que o desejado, manter o PDF original
                    os.rename(output_file, file_path)

            # Exibir mensagem de sucesso
            self.show_info("Sucesso!", "PDFs comprimidos com sucesso.")
        except Exception as e:
            # Exibir mensagem de erro em caso de problemas
            self.show_info("Erro!", str(e))

    # Função para exibir uma janela de mensagem informativa
    def show_info(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)
        popup.configure(background="black")
        tk.Label(popup, text=message, foreground="blue", background="black").pack()
        tk.Button(popup, text="OK", command=popup.destroy).pack()

# Função principal do programa
if __name__ == "__main__":
    root = tk.Tk() # Criar a janela principal
    root.configure(background="black") # Definir o fundo da janela como preto
    app = PDFCompressorApp(root) # Criar a instância da interface gráfica
    root.mainloop() # Iniciar o loop principal da interface
