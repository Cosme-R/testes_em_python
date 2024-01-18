
#comprimi um video para o tamanho selecionado 
import os
import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip

# Criar a classe que representa a interface gráfica do programa
class VideoCompressorApp:
    def __init__(self, root):
        # Configurar a janela principal com o título "Video Compressor" e cor de fundo preta
        self.root = root
        self.root.title("Video Compressor")
        self.root.configure(background="black")
        
        # Inicializar as variáveis para guardar os caminhos dos arquivos, pasta de saída e tamanho desejado
        self.file_paths = [] # Guardará os caminhos dos vídeos selecionados
        self.output_folder = tk.StringVar() # Guardará o caminho da pasta de saída
        self.target_size = tk.StringVar() # Guardará o tamanho desejado para os vídeos

        # Chamar a função para criar os elementos da interface
        self.create_widgets()

    # Função para criar os elementos da interface gráfica
    def create_widgets(self):
        # Botão para selecionar os vídeos
        btn_select = tk.Button(self.root, text="Selecionar Vídeos", command=self.select_files)
        btn_select.pack(pady=10)

        # Botão para selecionar a pasta de saída
        btn_output = tk.Button(self.root, text="Selecionar Pasta de Saída", command=self.choose_output_folder)
        btn_output.pack(pady=10)

        # Campo para inserir o tamanho desejado (em MB)
        label_target_size = tk.Label(self.root, text="Tamanho desejado (MB):", foreground="blue", background="black")
        label_target_size.pack()
        entry_target_size = tk.Entry(self.root, textvariable=self.target_size)
        entry_target_size.pack()

        # Botão para iniciar a compressão
        btn_compress = tk.Button(self.root, text="Comprimir Vídeos", command=self.compress_videos)
        btn_compress.pack(pady=20)

    # Função para abrir a janela de seleção de arquivos e guardar os caminhos dos vídeos selecionados
    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Arquivos de vídeo", "*.mp4 *.avi")])
        self.file_paths.extend(file_paths)

    # Função para abrir a janela de seleção de pasta e guardar o caminho da pasta de saída
    def choose_output_folder(self):
        self.output_folder.set(filedialog.askdirectory())

    # Função para comprimir os vídeos com base no tamanho desejado
    def compress_videos(self):
        try:
            # Pegar o caminho da pasta de saída e o tamanho desejado do usuário
            output_folder = self.output_folder.get()
            target_size_mb = float(self.target_size.get())
            target_size_bytes = target_size_mb * 1024 * 1024 # Converter o tamanho para bytes

            # Verificar se a pasta de saída existe
            if not os.path.isdir(output_folder):
                raise FileNotFoundError("O diretório de saída selecionado não foi encontrado.")

            # Loop para comprimir cada vídeo selecionado
            for file_path in self.file_paths:
                # Verificar se o arquivo de vídeo existe
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f"O arquivo de vídeo '{file_path}' não foi encontrado.")

                # Carregar o vídeo e obter sua duração e tamanho atual
                video = VideoFileClip(file_path)
                video_duration = video.duration
                video_size_bytes = os.path.getsize(file_path)

                # Verificar se o tamanho atual já está menor ou igual ao tamanho desejado
                if video_size_bytes <= target_size_bytes:
                    video.reader.close()
                    video.audio.reader.close_proc()
                    video.close()
                    continue

                # Calcular o fator de compressão para atingir o tamanho desejado
                compression_factor = target_size_bytes / video_size_bytes

                # Definir o caminho do arquivo comprimido
                compressed_file = os.path.join(output_folder, f"compressed_{os.path.basename(file_path)}")

                # Escrever o vídeo comprimido no arquivo de saída com a taxa de bits ajustada
                video.write_videofile(compressed_file, codec="libx264", bitrate=str(int(video.fps * video.w * video.h * compression_factor)))

                # Fechar os leitores de vídeo e áudio para liberar recursos
                video.reader.close()
                video.audio.reader.close_proc()
                video.close()

            # Exibir mensagem de sucesso
            self.show_info("Sucesso!", "Vídeos comprimidos com sucesso.")
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
    app = VideoCompressorApp(root) # Criar a instância da interface gráfica
    root.mainloop() # Iniciar o loop principal da interface
