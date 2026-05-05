import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import yt_dlp
import threading
import os
import requests
import subprocess
from PIL import Image
from io import BytesIO

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class YoutubeUltimateDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader Pro - Personalizzato")
        self.geometry("750x750")

        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.ffmpeg_path = "ffmpeg" # Di default cerca nel sistema

        # --- UI ---
        self.label_title = ctk.CTkLabel(self, text="YT DOWNLOADER", font=("Roboto", 28, "bold"), text_color="#FF0000")
        self.label_title.pack(pady=10)

        # URL Input
        self.url_frame = ctk.CTkFrame(self)
        self.url_frame.pack(pady=5, padx=20, fill="x")
        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="Incolla URL Video...", height=35)
        self.url_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        self.search_btn = ctk.CTkButton(self.url_frame, text="🔍 Cerca", width=80, command=self.load_video_info)
        self.search_btn.pack(side="right", padx=10)

        # Nome File Personalizzato
        self.name_frame = ctk.CTkFrame(self)
        self.name_frame.pack(pady=5, padx=20, fill="x")
        ctk.CTkLabel(self.name_frame, text="Nome File:").pack(side="left", padx=10)
        self.filename_entry = ctk.CTkEntry(self.name_frame, placeholder_text="Lascia vuoto per titolo originale...", height=35)
        self.filename_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        # Preview Area
        self.preview_frame = ctk.CTkFrame(self, fg_color="#222")
        self.preview_frame.pack(pady=10, padx=20, fill="x")
        self.thumbnail_label = ctk.CTkLabel(self.preview_frame, text="Anteprima")
        self.thumbnail_label.pack(side="left", padx=15, pady=10)
        self.video_title_label = ctk.CTkLabel(self.preview_frame, text="Nessun video caricato", font=("Roboto", 13), wraplength=450)
        self.video_title_label.pack(side="left", padx=10)

        # Settings
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(pady=10, padx=20, fill="x")

        self.quality_menu = ctk.CTkOptionMenu(self.settings_frame, values=["Migliore", "1080p", "720p", "480p", "Solo Audio (MP3)"])
        self.quality_menu.set("1080p")
        self.quality_menu.grid(row=0, column=0, padx=15, pady=15)

        self.path_btn = ctk.CTkButton(self.settings_frame, text="📁 Cartella Salva", fg_color="#444", command=self.select_path)
        self.path_btn.grid(row=0, column=1, padx=15, pady=15)

        self.ffmpeg_btn = ctk.CTkButton(self.settings_frame, text="⚙️ Seleziona FFmpeg.exe", fg_color="#444", command=self.select_ffmpeg_manually)
        self.ffmpeg_btn.grid(row=0, column=2, padx=15, pady=15)

        # Progress
        self.progress_bar = ctk.CTkProgressBar(self, width=600)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(self, text="Verifica FFmpeg...", font=("Roboto", 12))
        self.status_label.pack()

        # Download Buttons
        self.download_btn = ctk.CTkButton(self, text="SCARICA ORA", command=self.start_download_thread, 
                                          font=("Roboto", 18, "bold"), fg_color="#FF0000", hover_color="#CC0000", height=50)
        self.download_btn.pack(pady=10, padx=20, fill="x")

        self.open_folder_btn = ctk.CTkButton(self, text="Apri Cartella Download", command=self.open_folder, state="disabled")
        self.open_folder_btn.pack(pady=5)

        self.check_ffmpeg()

    def check_ffmpeg(self):
        try:
            subprocess.run([self.ffmpeg_path, "-version"], capture_output=True, check=True)
            self.status_label.configure(text="FFmpeg OK: Tutte le funzioni attive.", text_color="green")
            self.ffmpeg_available = True
        except:
            self.status_label.configure(text="FFmpeg NON TROVATO. Selezionalo manualmente per MP3 e 1080p.", text_color="orange")
            self.ffmpeg_available = False

    def select_ffmpeg_manually(self):
        path = filedialog.askopenfilename(title="Seleziona il file ffmpeg.exe", filetypes=[("Executable", "*.exe")])
        if path:
            self.ffmpeg_path = path
            self.check_ffmpeg()

    def select_path(self):
        path = filedialog.askdirectory()
        if path: self.download_path = path

    def open_folder(self):
        os.startfile(self.download_path)

    def load_video_info(self):
        url = self.url_entry.get()
        if not url: return
        threading.Thread(target=self._fetch_info, args=(url,), daemon=True).start()

    def _fetch_info(self, url):
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Video')
                self.video_title_label.configure(text=title[:100])
                thumb_url = info.get('thumbnail')
                resp = requests.get(thumb_url)
                img = Image.open(BytesIO(resp.content))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(160, 90))
                self.thumbnail_label.configure(image=ctk_img, text="")
        except: self.status_label.configure(text="Errore link", text_color="red")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            p_str = d.get('_percent_str', '0%').replace('%','')
            try:
                val = float(p_str) / 100
                self.progress_bar.set(val)
                self.status_label.configure(text=f"Download: {p_str}% - Vel: {d.get('_speed_str', '??')}")
            except: pass

    def start_download_thread(self):
        threading.Thread(target=self.download_video, daemon=True).start()

    def download_video(self):
        url = self.url_entry.get()
        if not url: return

        custom_name = self.filename_entry.get().strip()
        # Se l'utente ha inserito un nome, lo usiamo, altrimenti usiamo il titolo di YT
        template = f"{custom_name}.%(ext)s" if custom_name else "%(title)s.%(ext)s"
        
        ydl_opts = {
            'outtmpl': os.path.join(self.download_path, template),
            'progress_hooks': [self.progress_hook],
            'ffmpeg_location': self.ffmpeg_path,
        }

        choice = self.quality_menu.get()
        if choice == "Solo Audio (MP3)":
            if not self.ffmpeg_available:
                messagebox.showerror("FFmpeg Mancante", "Seleziona ffmpeg.exe prima di scaricare MP3.")
                return
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
            })
        else:
            if not self.ffmpeg_available:
                ydl_opts['format'] = 'best' # Fallback 720p
            else:
                height = choice.replace("p", "")
                ydl_opts['format'] = 'bestvideo+bestaudio/best' if height == "Migliore" else f'bestvideo[height<={height}]+bestaudio/best'

        try:
            self.download_btn.configure(state="disabled")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.configure(text="DOWNLOAD COMPLETATO!", text_color="green")
            self.open_folder_btn.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
        finally:
            self.download_btn.configure(state="normal")

if __name__ == "__main__":
    app = YoutubeUltimateDownloader()
    app.mainloop()