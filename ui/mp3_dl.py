import customtkinter as ctk
import threading
import datetime
from settings.config import config
from download.video_worker import DownloadWorker
from backend.ytdlp_engine import get_video_info
from backend.history import add_history
from utils.logger_util import app_logger

class MP3DownloaderFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.header = ctk.CTkLabel(self, text="♫ Audio (MP3) Downloader", font=ctk.CTkFont(size=28, weight="bold"), text_color="#A855F7")
        self.header.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=30)
        
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Video/Audio URL...", height=40, corner_radius=8)
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.fetch_btn = ctk.CTkButton(self.input_frame, text="Fetch Metadata", height=40, width=120, corner_radius=8, command=self.fetch_metadata)
        self.fetch_btn.grid(row=0, column=1)

        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.content_frame, text="Ready.", font=ctk.CTkFont(size=16, weight="bold"), wraplength=450)
        self.title_label.pack(pady=20, padx=20)
        
        # Audio Quality
        format_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        format_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(format_frame, text="Audio Quality:").pack(side="left", padx=5)
        self.quality_menu = ctk.CTkOptionMenu(format_frame, values=["320 kbps", "256 kbps", "192 kbps", "128 kbps"])
        self.quality_menu.pack(side="left", padx=5)
        
        ctk.CTkLabel(format_frame, text="Format:").pack(side="left", padx=(20, 5))
        self.format_menu = ctk.CTkOptionMenu(format_frame, values=["MP3", "M4A", "FLAC", "WAV", "OGG"])
        self.format_menu.pack(side="left", padx=5)
        
        self.embed_thumb_var = ctk.BooleanVar(value=True)
        self.embed_thumb = ctk.CTkCheckBox(self.content_frame, text="Embed Cover Art (Requires MP3/M4A/FLAC)", variable=self.embed_thumb_var)
        self.embed_thumb.pack(anchor="w", padx=25, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.content_frame, height=10)
        self.progress_bar.pack(side="bottom", fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)

        self.download_btn = ctk.CTkButton(self.content_frame, text="Download Audio", height=50, fg_color="#F59E0B", hover_color="#D97706", font=ctk.CTkFont(weight="bold"), command=self.start_download)
        self.download_btn.pack(side="bottom", fill="x", padx=20, pady=20)

        self.active_info = None

    def fetch_metadata(self):
        url = self.url_entry.get().strip()
        if not url: return
        self.fetch_btn.configure(text="Loading...", state="disabled")
        self.title_label.configure(text="Fetching info, please wait...")
        
        def runner():
            try:
                info = get_video_info(url)
                self.master.after(0, self.update_ui, info)
            except Exception as e:
                self.master.after(0, lambda: self.title_label.configure(text=f"Error: {e}"))
            finally:
                self.master.after(0, lambda: self.fetch_btn.configure(text="Fetch Metadata", state="normal"))
                
        threading.Thread(target=runner, daemon=True).start()

    def update_ui(self, info):
        self.active_info = info
        self.title_label.configure(text=f"Title: {info.get('title', 'Unknown')}")

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url or not self.active_info:
            return
            
        self.download_btn.configure(text="Downloading...", state="disabled", fg_color="#F59E0B")
        self.progress_bar.set(0)
        
        def _on_progress(d):
            if d['status'] == 'downloading':
                percent = d.get('percent', 0) / 100
                self.master.after(0, lambda: self.progress_bar.set(percent))
                
        def _on_error(err):
            app_logger.error(f"Audio DL Error: {err}")
            self.master.after(0, lambda: self.download_btn.configure(text="Error! Retry?", fg_color="#EF4444", state="normal"))
            self.master.after(4000, lambda: self.download_btn.configure(text="Download Audio", fg_color="#F59E0B"))

        def _on_finished(info):
            hist_item = {
                "title": self.active_info.get("title", "Unknown"),
                "url": url,
                "date": str(datetime.datetime.now()),
                "status": "Completed",
                "thumbnail": self.active_info.get("thumbnail")
            }
            self.master.after(0, lambda: add_history(hist_item))
            self.master.after(0, lambda: self.master.frames["downloads"].refresh())
            self.master.after(0, lambda: self.progress_bar.set(1))
            self.master.after(0, lambda: self.download_btn.configure(text="Finished!", fg_color="#10B981", state="normal"))
            self.master.after(3000, lambda: self.download_btn.configure(text="Download Audio", fg_color="#F59E0B"))

        quality = self.quality_menu.get().split(" ")[0]
        ext = self.format_menu.get().lower()
        
        opts = {
            'outtmpl': f"{config.get('download_dir', 'Downloads')}/%(title)s.%(ext)s",
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': ext,
                'preferredquality': quality,
            }],
        }
        
        if self.embed_thumb_var.get() and ext in ["mp3", "m4a", "flac"]:
            opts['writethumbnail'] = True
            opts['postprocessors'].append({'key': 'EmbedThumbnail'})
            
        worker = DownloadWorker(url, opts, _on_progress, _on_finished, _on_error)
        worker.start()
