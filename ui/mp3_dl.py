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
        
        self.header = ctk.CTkLabel(self, text="✎ Audio (MP3) Downloader", font=ctk.CTkFont(family="Ink Free", size=36, weight="bold"), text_color="#FFB347")
        self.header.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=30)
        
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="✎ Paste Video/Audio URL...", height=45, font=ctk.CTkFont(family="Ink Free", size=18), corner_radius=15, border_width=2, border_color="#F5F5DC", fg_color="#3E3C38", text_color="#F5F5DC")
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.fetch_btn = ctk.CTkButton(self.input_frame, text="Fetch Metadata", height=45, width=140, corner_radius=15, fg_color="transparent", border_width=2, border_color="#87CEEB", text_color="#87CEEB", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=18, weight="bold"), command=self.fetch_metadata)
        self.fetch_btn.grid(row=0, column=1)

        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#FFB347")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self.content_frame, text="✎ Ready.", font=ctk.CTkFont(family="Ink Free", size=20, weight="bold"), text_color="#F5F5DC", wraplength=450)
        self.title_label.pack(pady=20, padx=20)
        
        # Audio Quality
        format_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        format_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(format_frame, text="Audio Quality:", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB").pack(side="left", padx=5)
        self.quality_menu = ctk.CTkOptionMenu(format_frame, values=["320 kbps", "256 kbps", "192 kbps", "128 kbps"], font=ctk.CTkFont(family="Ink Free", size=14), fg_color="#3E3C38", button_color="#5E4C38", corner_radius=10)
        self.quality_menu.pack(side="left", padx=5)
        
        ctk.CTkLabel(format_frame, text="Format:", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB").pack(side="left", padx=(20, 5))
        self.format_menu = ctk.CTkOptionMenu(format_frame, values=["MP3", "M4A", "FLAC", "WAV", "OGG"], font=ctk.CTkFont(family="Ink Free", size=14), fg_color="#3E3C38", button_color="#5E4C38", corner_radius=10)
        self.format_menu.pack(side="left", padx=5)
        
        self.embed_thumb_var = ctk.BooleanVar(value=True)
        self.embed_thumb = ctk.CTkCheckBox(self.content_frame, text="Embed Cover Art (Requires MP3/M4A/FLAC)", variable=self.embed_thumb_var, font=ctk.CTkFont(family="Ink Free", size=16), text_color="#F5F5DC", fg_color="#FFB347", border_color="#FFB347", hover_color="#5E4C38")
        self.embed_thumb.pack(anchor="w", padx=25, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.content_frame, height=12, progress_color="#FFB347")
        self.progress_bar.pack(side="bottom", fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)

        self.download_btn = ctk.CTkButton(self.content_frame, text="Download Audio", height=55, corner_radius=15, fg_color="transparent", border_width=2, border_color="#FFB347", text_color="#FFB347", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=20, weight="bold"), command=self.start_download)
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
            
        self.download_btn.configure(text="Starting... (Click to Pause)", state="normal", fg_color="#F59E0B", text_color="#1E1C1A", command=self.toggle_pause)
        self.is_paused = False
        self.progress_bar.set(0)
        
        def _on_progress(d):
            if d['status'] == 'downloading':
                percent = d.get('percent', 0) / 100
                speed = d.get('speed', 0)
                def update_stats():
                    try:
                        self.progress_bar.set(percent)
                        if not getattr(self, 'is_paused', False):
                            self.download_btn.configure(text=f"Downloading... {int(percent*100)}%", text_color="#1E1C1A")
                    except:
                        pass
                self.master.after(0, update_stats)
                
        def _on_error(err):
            app_logger.error(f"Audio DL Error: {err}")
            self.master.after(0, lambda: self.download_btn.configure(text="Error! Retry?", fg_color="#EF4444", text_color="#F5F5DC", state="normal", command=self.start_download))
            self.master.after(4000, lambda: self.download_btn.configure(text="Download Audio", fg_color="transparent", text_color="#FFB347"))

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
            self.master.after(0, lambda: self.download_btn.configure(text="Finished!", fg_color="#10B981", text_color="#F5F5DC", state="normal", command=self.start_download))
            self.master.after(3000, lambda: self.download_btn.configure(text="Download Audio", fg_color="transparent", text_color="#FFB347"))

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
        self.active_worker = worker
        worker.start()

    def toggle_pause(self):
        if not hasattr(self, 'active_worker') or not self.active_worker:
            return
            
        if self.is_paused:
            self.active_worker.resume()
            self.is_paused = False
            self.download_btn.configure(text="Resuming...", fg_color="#F59E0B", text_color="#1E1C1A")
        else:
            self.active_worker.pause()
            self.is_paused = True
            self.download_btn.configure(text="Paused (Click to Resume)", fg_color="#3B82F6", text_color="#F5F5DC")
