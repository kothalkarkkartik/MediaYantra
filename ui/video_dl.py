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
        self.header = ctk.CTkLabel(self, text="✎ Video Downloader", font=ctk.CTkFont(family="Ink Free", size=36, weight="bold"), text_color="#FFB347")
        self.header.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=30)
        
        # URL Input Area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="✎ Paste Video URL...", height=45, font=ctk.CTkFont(family="Ink Free", size=18), corner_radius=15, border_width=2, border_color="#F5F5DC", fg_color="#3E3C38", text_color="#F5F5DC")
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.fetch_btn = ctk.CTkButton(self.input_frame, text="Fetch Metadata", height=45, width=140, corner_radius=15, fg_color="transparent", border_width=2, border_color="#87CEEB", text_color="#87CEEB", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=18, weight="bold"))
        self.fetch_btn.grid(row=0, column=1)
        
        # Content Area - Two Columns (Left: Thumbnail & Info, Right: Options)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=1, uniform="col")
        self.content_frame.grid_columnconfigure(1, weight=1, uniform="col")
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # --- Left Column: Info --- #
        self.info_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#87CEEB")
        self.info_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.thumb_label = ctk.CTkLabel(self.info_frame, text="✎ Thumbnail Preview", font=ctk.CTkFont(family="Ink Free", size=18), height=200, fg_color="#3E3C38", corner_radius=15)
        self.thumb_label.pack(fill="x", padx=15, pady=15)
        
        self.title_label = ctk.CTkLabel(self.info_frame, text="Title: Not loaded", font=ctk.CTkFont(family="Ink Free", size=18, weight="bold"), text_color="#F5F5DC", wraplength=350, justify="left")
        self.title_label.pack(anchor="w", padx=15, pady=5)
        
        self.uploader_label = ctk.CTkLabel(self.info_frame, text="Uploader: -", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB")
        self.uploader_label.pack(anchor="w", padx=15, pady=2)
        
        self.duration_label = ctk.CTkLabel(self.info_frame, text="Duration: -", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB")
        self.duration_label.pack(anchor="w", padx=15, pady=2)
        
        self.size_label = ctk.CTkLabel(self.info_frame, text="Estimated Size: -", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB")
        self.size_label.pack(anchor="w", padx=15, pady=2)
        
        # --- Right Column: Options --- #
        self.options_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#FFB347")
        self.options_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(self.options_frame, text="✎ Download Options", font=ctk.CTkFont(family="Ink Free", size=22, weight="bold"), text_color="#FFB347").pack(pady=(15, 10), padx=15, anchor="w")
        
        # Quality Selector
        ctk.CTkLabel(self.options_frame, text="Resolution:", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB").pack(anchor="w", padx=15)
        self.quality_var = ctk.StringVar(value="Best Quality")
        self.quality_menu = ctk.CTkOptionMenu(self.options_frame, values=["Best Quality", "4K", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p", "Audio Only"], variable=self.quality_var, font=ctk.CTkFont(family="Ink Free", size=14), fg_color="#3E3C38", button_color="#5E4C38", corner_radius=10)
        self.quality_menu.pack(fill="x", padx=15, pady=(0, 10))
        
        # Format Selector
        ctk.CTkLabel(self.options_frame, text="Format:", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB").pack(anchor="w", padx=15)
        self.format_menu = ctk.CTkOptionMenu(self.options_frame, values=["MP4", "MKV", "WEBM", "MOV"], font=ctk.CTkFont(family="Ink Free", size=14), fg_color="#3E3C38", button_color="#5E4C38", corner_radius=10)
        self.format_menu.pack(fill="x", padx=15, pady=(0, 10))
        
        # Checkboxes for embeddings
        self.embed_thumb_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.options_frame, text="Embed Thumbnail", variable=self.embed_thumb_var, font=ctk.CTkFont(family="Ink Free", size=16), text_color="#F5F5DC", fg_color="#FFB347", border_color="#FFB347", hover_color="#5E4C38").pack(anchor="w", padx=15, pady=5)
        
        self.embed_meta_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.options_frame, text="Embed Metadata", variable=self.embed_meta_var, font=ctk.CTkFont(family="Ink Free", size=16), text_color="#F5F5DC", fg_color="#FFB347", border_color="#FFB347", hover_color="#5E4C38").pack(anchor="w", padx=15, pady=5)
        
        self.embed_subs_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self.options_frame, text="Embed Subtitles", variable=self.embed_subs_var, font=ctk.CTkFont(family="Ink Free", size=16), text_color="#F5F5DC", fg_color="#FFB347", border_color="#FFB347", hover_color="#5E4C38").pack(anchor="w", padx=15, pady=5)

        # Download Button
        self.download_btn = ctk.CTkButton(self.options_frame, text="Download Video", height=55, corner_radius=15, fg_color="transparent", border_width=2, border_color="#8FBC8F", text_color="#8FBC8F", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=20, weight="bold"))
        self.download_btn.pack(side="bottom", fill="x", padx=15, pady=15)
        
        self.progress_bar = ctk.CTkProgressBar(self.options_frame, height=12, progress_color="#8FBC8F")
        self.progress_bar.pack(side="bottom", fill="x", padx=15, pady=(0, 5))
        self.progress_bar.set(0)
        
        self.location_label = ctk.CTkLabel(self.options_frame, text=f"Location: {config.get('download_dir', 'Downloads')}", font=ctk.CTkFont(family="Ink Free", size=14), text_color="#A3A3A3")
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
        self.download_btn.configure(text="Starting... (Click to Pause)", fg_color="#F59E0B", text_color="#1E1C1A", state="normal", command=self.toggle_pause)
        self.is_paused = False
        
        def _on_progress(d):
            if d['status'] == 'downloading':
                percent = d.get('percent', 0) / 100
                speed = d.get('speed', 0)
                
                def update_stats():
                    try:
                        self.progress_bar.set(percent)
                        if not getattr(self, 'is_paused', False):
                            self.download_btn.configure(text=f"{format_size(speed)}/s - {int(percent*100)}%", text_color="#1E1C1A")
                    except:
                        pass
                self.master.after(0, update_stats)
                
            elif d['status'] == 'finished':
                def update_done():
                    self.progress_bar.set(1)
                    self.download_btn.configure(text="Finished!", fg_color="#10B981", text_color="#F5F5DC", state="normal", command=self.start_download)
                    # Reset button after 3 seconds so user can download again
                    self.master.after(3000, self._reset_download_btn)
                self.master.after(0, update_done)
                
        def _on_error(err):
            app_logger.error(str(err))
            def update_err():
                self.download_btn.configure(text="Error! Retry?", fg_color="#EF4444", text_color="#F5F5DC", state="normal", command=self.start_download)
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

    def _reset_download_btn(self):
        """Reset the download button to its original state."""
        try:
            self.download_btn.configure(
                text="Download Video",
                fg_color="transparent",
                text_color="#8FBC8F",
                hover_color="#5E4C38",
                state="normal",
                command=self.start_download
            )
            self.progress_bar.set(0)
        except:
            pass
