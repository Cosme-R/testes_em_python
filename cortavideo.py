#programa pra dividir um video logo em diversos videos menores 
import os
import tkinter as tk
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import shutil

class VideoCutterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("divisor de video ")
        self.root.configure(background="black")
        self.file_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.segment_duration = tk.StringVar()
        
        self.create_widgets()

    def create_widgets(self):
        #  selecionar o vídeo
        label_select = tk.Label(self.root, text="Selecione o vídeo:", foreground="blue", background="black")
        label_select.pack()
        btn_browse = tk.Button(self.root, text="Buscar", command=self.browse_file)
        btn_browse.pack()

        #  campo para inserir o diretório de saída
        label_output = tk.Label(self.root, text="Selecione a pasta de saída:", foreground="blue", background="black")
        label_output.pack()
        btn_output = tk.Button(self.root, text="Selecionar", command=self.choose_output_folder)
        btn_output.pack()

        # Campo para inserir o tamanho do segmento em segundos
        label_segment_duration = tk.Label(self.root, text="Tamanho do segmento (em segundos):", foreground="blue", background="black")
        label_segment_duration.pack()
        entry_segment_duration = tk.Entry(self.root, textvariable=self.segment_duration)
        entry_segment_duration.pack()

        # Botão para cortar o vídeo
        btn_cut = tk.Button(self.root, text="Cortar", command=self.cut_video)
        btn_cut.pack()

    def browse_file(self):
        self.file_path.set(filedialog.askopenfilename(filetypes=[("Arquivos de vídeo", "*.mp4 *.avi")]))

    def choose_output_folder(self):
        self.output_folder.set(filedialog.askdirectory())

    def cut_video(self):
        try:
            file_path = self.file_path.get()
            output_folder = self.output_folder.get()
            segment_duration = float(self.segment_duration.get())

            if not os.path.isfile(file_path):
                raise FileNotFoundError("O arquivo de vídeo selecionado não foi encontrado.")

            if not os.path.isdir(output_folder):
                raise FileNotFoundError("O diretório de saída selecionado não foi encontrado.")

            video = VideoFileClip(file_path)
            video_duration = video.duration

            if segment_duration <= 0 or segment_duration >= video_duration:
                raise ValueError("O tamanho do segmento deve ser maior que zero e menor que a duração do vídeo.")

            segment_count = int(video_duration // segment_duration)
            remaining_time = video_duration % segment_duration

            for i in range(segment_count):
                start_time = i * segment_duration
                end_time = start_time + segment_duration
                output_file = os.path.join(output_folder, f"cut_video_{i + 1}.mp4")
                ffmpeg_extract_subclip(file_path, start_time, end_time, targetname=output_file)

            if remaining_time > 0:
                start_time = segment_count * segment_duration
                end_time = video_duration
                output_file = os.path.join(output_folder, f"cut_video_{segment_count + 1}.mp4")
                ffmpeg_extract_subclip(file_path, start_time, end_time, targetname=output_file)

            video.reader.close()
            video.audio.reader.close_proc()
            video.close()

            self.show_info("Sucesso!", f"Vídeo cortado em {segment_count + 1} segmentos.")
        except Exception as e:
            self.show_info("Erro!", str(e))

    def show_info(self, title, message):
        popup = tk.Toplevel()
        popup.title(title)
        popup.configure(background="black")
        tk.Label(popup, text=message, foreground="blue", background="black").pack()
        tk.Button(popup, text="OK", command=popup.destroy).pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background="black")
    app = VideoCutterApp(root)
    root.mainloop()
