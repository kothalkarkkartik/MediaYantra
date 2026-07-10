import customtkinter as ctk
import threading
import requests
import datetime
from io import BytesIO
from PIL import Image
from settings.config import config
from download.video_worker import DownloadWorker
from backend.ytdlp_engine import get_video_info
from utils.helpers import format_duration, format_size
from backend.history import add_history
from utils.logger_util import app_logger

class VideoDownloaderFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="⯈ Video Downloader", font=ctk.CTkFont(size=28, weight="bold"), text_color="#A855F7")
        self.header.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=30)
        
        # URL Input Area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Video URL...", height=40, corner_radius=8)
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.fetch_btn = ctk.CTkButton(self.input_frame, text="Fetch Metadata", height=40, width=120, corner_radius=8, fg_color="#3B82F6", hover_color="#2563EB")
        self.fetch_btn.grid(row=0, column=1)
        
        # Content Area - Two Columns (Left: Thumbnail & Info, Right: Options)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1, uniform="col")
        self.content_frame.grid_columnconfigure(1, weight=1, uniform="col")
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # --- Left Column: Info --- #
        self.info_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.thumb_label = ctk.CTkLabel(self.info_frame, text="Thumbnail Preview", height=200, fg_color="gray20", corner_radius=8)
        self.thumb_label.pack(fill="x", padx=15, pady=15)
        
        self.title_label = ctk.CTkLabel(self.info_frame, text="Title: Not loaded", font=ctk.CTkFont(weight="bold"), wraplength=350, justify="left")
        self.title_label.pack(anchor="w", padx=15, pady=5)
        
        self.uploader_label = ctk.CTkLabel(self.info_frame, text="Uploader: -")
        self.uploader_label.pack(anchor="w", padx=15, pady=2)
        
        self.duration_label = ctk.CTkLabel(self.info_frame, text="Duration: -")
        self.duration_label.pack(anchor="w", padx=15, pady=2)
        
        self.size_label = ctk.CTkLabel(self.info_frame, text="Estimated Size: -")
        self.size_label.pack(anchor="w", padx=15, pady=2)
        
        # --- Right Column: Options --- #
        self.options_frame = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.options_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(self.options_frame, text="Download Options", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15, 10), padx=15, anchor="w")
        
        # Quality Selector
        ctk.CTkLabel(self.options_frame, text="Resolution:").pack(anchor="w", padx=15)
        self.quality_var = ctk.StringVar(value="Best Quality")
        self.quality_menu = ctk.CTkOptionMenu(self.options_frame, values=["Best Quality", "4K", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p", "Audio Only"], variable=self.quality_var)
        self.quality_menu.pack(fill="x", padx=15, pady=(0, 10))
        
        # Format Selector
        ctk.CTkLabel(self.options_frame, text="Format:").pack(anchor="w", padx=15)
        self.format_menu = ctk.CTkOptionMenu(self.options_frame, values=["MP4", "MKV", "WEBM", "MOV"])
        self.format_menu.pack(fill="x", padx=15, pady=(0, 10))
        
        # Checkboxes for embeddings
        self.embed_thumb_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.options_frame, text="Embed Thumbnail", variable=self.embed_thumb_var).pack(anchor="w", padx=15, pady=5)
        
        self.embed_meta_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.options_frame, text="Embed Metadata", variable=self.embed_meta_var).pack(anchor="w", padx=15, pady=5)
        
        self.embed_subs_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self.options_frame, text="Embed Subtitles", variable=self.embed_subs_var).pack(anchor="w", padx=15, pady=5)

        # Download Button
        self.download_btn = ctk.CTkButton(self.options_frame, text="Download Video", height=50, corner_radius=10, fg_color="#10B981", hover_color="#059669", font=ctk.CTkFont(size=16, weight="bold"))
        self.download_btn.pack(side="bottom", fill="x", padx=15, pady=15)
        
        self.progress_bar = ctk.CTkProgressBar(self.options_frame, height=10)
        self.progress_bar.pack(side="bottom", fill="x", padx=15, pady=(0, 5))
        self.progress_bar.set(0)
        
        self.location_label = ctk.CTkLabel(self.options_frame, text=f"Location: {config.get('download_dir', 'Downloads')}", text_color="gray50")
        self.location_label.pack(side="bottom", pady=5)
        
        self.fetch_btn.configure(command=self.fetch_metadata)
        self.download_btn.configure(command=self.start_download)
        self.active_info = None

    def fetch_metadata(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        self.fetch_btn.configure(text="Fetching...", state="disabled")
        
        def runner():
            try:
                info = get_video_info(url)
                self.master.after(0, self.update_ui, info)
            except Exception as e:
                self.master.after(0, lambda: self.title_label.configure(text=f"Error: {str(e)[:50]}..."))
            finally:
                self.master.after(0, lambda: self.fetch_btn.configure(text="Fetch Metadata", state="normal"))
                
        threading.Thread(target=runner, daemon=True).start()

    def update_ui(self, info):
        self.active_info = info
        self.title_label.configure(text=f"Title: {info.get('title', 'Unknown')}")
        self.uploader_label.configure(text=f"Uploader: {info.get('uploader', '-')}")
        self.duration_label.configure(text=f"Duration: {format_duration(info.get('duration', 0))}")
        self.size_label.configure(text="Estimated Size: Ready to download")
        
        thumb_url = info.get('thumbnail')
        if thumb_url:
            def _fetch_thumb():
                try:
                    response = requests.get(thumb_url)
                    img = Image.open(BytesIO(response.content))
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 170))
                    self.master.after(0, lambda: self.thumb_label.configure(image=ctk_img, text=""))
                except:
                    pass
            threading.Thread(target=_fetch_thumb, daemon=True).start()
            
    def start_download(self):
        if not self.active_info:
            return
        self.download_btn.configure(text="Starting...", fg_color="#F59E0B", state="disabled")
        
        def _on_progress(d):
            if d['status'] == 'downloading':
                percent = d.get('percent', 0) / 100
                speed = d.get('speed', 0)
                
                def update_stats():
                    try:
                        self.progress_bar.set(percent)
                        self.download_btn.configure(text=f"{format_size(speed)}/s - {int(percent*100)}%")
                    except:
                        pass
                self.master.after(0, update_stats)
                
            elif d['status'] == 'finished':
                def update_done():
                    self.progress_bar.set(1)
                    self.download_btn.configure(text="Finished!", fg_color="#10B981", state="normal")
                    # Reset button after 3 seconds so user can download again
                    self.master.after(3000, self._reset_download_btn)
                self.master.after(0, update_done)
                
        def _on_error(err):
            app_logger.error(str(err))
            def update_err():
                self.download_btn.configure(text="Error! Retry?", fg_color="#EF4444", state="normal")
                # Reset button after 4 seconds
                self.master.after(4000, self._reset_download_btn)
            self.master.after(0, update_err)
            
        url = self.url_entry.get().strip()
        
        def _on_finished(info):
            app_logger.debug("Download completed successfully.")
            
            # Using the pre-captured 'url' closure variable instead of querying Tkinter across threads!
            hist_item = {
                "title": self.active_info.get("title", "Unknown") if hasattr(self, 'active_info') and self.active_info else "Unknown",
                "url": url,
                "date": str(datetime.datetime.now()),
                "status": "Completed",
                "thumbnail": self.active_info.get("thumbnail") if hasattr(self, 'active_info') and self.active_info else None
            }
            self.master.after(0, lambda: add_history(hist_item))
            self.master.after(0, lambda: self.master.frames["downloads"].refresh())
            
        quality = self.quality_var.get()
        ext = self.format_menu.get().lower()
        
        yt_format = 'bestvideo+bestaudio/best'
        format_sort = None
        if quality == 'Audio Only':
            yt_format = 'bestaudio/best'
        elif quality != 'Best Quality':
            height = quality.replace('p', '')
            if height == '4K': height = '2160'
            # Use format_sort for reliable resolution selection (avoids hanging on unavailable formats)
            yt_format = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'
            format_sort = [f'res:{height}']
            
        opts = {
            'outtmpl': f"{config.get('download_dir', 'Downloads')}/%(title)s.%(ext)s",
            'format': yt_format,
            'merge_output_format': ext,
            'socket_timeout': 30,
        }
        if format_sort:
            opts['format_sort'] = format_sort
        
        worker = DownloadWorker(url, opts, _on_progress, _on_finished, _on_error)
        worker.start()

    def _reset_download_btn(self):
        """Reset the download button to its original state."""
        try:
            self.download_btn.configure(
                text="Download Video",
                fg_color="#10B981",
                hover_color="#059669",
                state="normal"
            )
            self.progress_bar.set(0)
        except:
            pass
