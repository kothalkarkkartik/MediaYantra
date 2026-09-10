import customtkinter as ctk
import threading
from backend.ytdlp_engine import get_playlist_info
from download.video_worker import DownloadWorker
from settings.config import config
from utils.logger_util import app_logger

class PlaylistDownloaderFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.header = ctk.CTkLabel(self, text="✎ Playlist Downloader", font=ctk.CTkFont(family="Ink Free", size=36, weight="bold"), text_color="#E6A8D7")
        self.header.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=30)
        
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=30, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="✎ Paste Playlist URL...", height=45, font=ctk.CTkFont(family="Ink Free", size=18), corner_radius=15, border_width=2, border_color="#F5F5DC", fg_color="#3E3C38", text_color="#F5F5DC")
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.fetch_btn = ctk.CTkButton(self.input_frame, text="Load Playlist", height=45, width=140, corner_radius=15, fg_color="transparent", border_width=2, border_color="#E6A8D7", text_color="#E6A8D7", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=18, weight="bold"), command=self.fetch_metadata)
        self.fetch_btn.grid(row=0, column=1)

        # Split content
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=2)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Playlist items 
        self.items_frame = ctk.CTkScrollableFrame(self.content_frame, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#E6A8D7")
        self.items_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.status_label = ctk.CTkLabel(self.items_frame, text="Videos will appear here after loading.", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB")
        self.status_label.pack(pady=20)
        
        # Options
        self.options_frame = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#87CEEB")
        self.options_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(self.options_frame, text="✎ Download Entire Playlist", font=ctk.CTkFont(family="Ink Free", size=22, weight="bold"), text_color="#87CEEB").pack(pady=15)
        
        ctk.CTkLabel(self.options_frame, text="Resolution:", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB").pack(anchor="w", padx=15, pady=(5,0))
        self.quality_var = ctk.StringVar(value="Best Quality")
        self.quality_menu = ctk.CTkOptionMenu(self.options_frame, values=["Best Quality", "1080p", "720p", "Audio Only"], variable=self.quality_var, font=ctk.CTkFont(family="Ink Free", size=14), fg_color="#3E3C38", button_color="#5E4C38", corner_radius=10)
        self.quality_menu.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(self.options_frame, text="Format:", font=ctk.CTkFont(family="Ink Free", size=16), text_color="#D1D5DB").pack(anchor="w", padx=15, pady=(5,0))
        self.format_menu = ctk.CTkOptionMenu(self.options_frame, values=["MP4", "MKV", "WEBM"], font=ctk.CTkFont(family="Ink Free", size=14), fg_color="#3E3C38", button_color="#5E4C38", corner_radius=10)
        self.format_menu.pack(fill="x", padx=15, pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(self.options_frame, height=12, progress_color="#8FBC8F")
        self.progress_bar.pack(side="bottom", fill="x", padx=15, pady=(0, 5))
        self.progress_bar.set(0)
        
        self.download_btn = ctk.CTkButton(self.options_frame, text="Download Playlist", height=55, corner_radius=15, fg_color="transparent", border_width=2, border_color="#8FBC8F", text_color="#8FBC8F", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=20, weight="bold"), command=self.start_download)
        self.download_btn.pack(side="bottom", fill="x", padx=15, pady=15)
        
        self.active_info = None

    def fetch_metadata(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        self.fetch_btn.configure(text="Loading...", state="disabled")
        self.status_label.configure(text="Fetching playlist info, please wait...")
        
        for widget in self.items_frame.winfo_children():
            if widget != self.status_label:
                widget.destroy()
        
        def runner():
            try:
                info = get_playlist_info(url)
                self.master.after(0, self.update_ui, info)
            except Exception as e:
                self.master.after(0, lambda: self.status_label.configure(text=f"Error: {e}"))
            finally:
                self.master.after(0, lambda: self.fetch_btn.configure(text="Load Playlist", state="normal"))
                
        threading.Thread(target=runner, daemon=True).start()

    def update_ui(self, info):
        self.active_info = info
        self.status_label.pack_forget()
        
        entries = info.get('entries', [])
        if not entries:
            self.status_label.configure(text="No videos found.")
            self.status_label.pack(pady=20)
            return
            
        for i, entry in enumerate(entries[:50]): # Display up to 50 items to prevent lag
            title = entry.get('title', 'Unknown Video')
            lbl = ctk.CTkLabel(self.items_frame, text=f"{i+1}. {title}", anchor="w", justify="left", font=ctk.CTkFont(family="Ink Free", size=15), text_color="#F5F5DC")
            lbl.pack(fill="x", padx=10, pady=2)
            
        if len(entries) > 50:
            lbl = ctk.CTkLabel(self.items_frame, text=f"...and {len(entries) - 50} more videos.", text_color="gray50")
            lbl.pack(pady=5)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        
        self.download_btn.configure(text="Starting... (Click to Pause)", state="normal", fg_color="#F59E0B", text_color="#1E1C1A", command=self.toggle_pause)
        self.is_paused = False
        
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
            self.master.after(0, lambda: self.download_btn.configure(text="Error! Retry?", fg_color="#EF4444", text_color="#F5F5DC", state="normal", command=self.start_download))
            app_logger.error(f"Playlist dl error: {err}")
            
        def _on_finished(info):
            self.master.after(0, lambda: self.progress_bar.set(1))
            self.master.after(0, lambda: self.download_btn.configure(text="Finished!", fg_color="#10B981", text_color="#F5F5DC", state="normal", command=self.start_download))
            # Reset after 3 seconds
            self.master.after(3000, lambda: self.download_btn.configure(text="Download Playlist", fg_color="transparent", text_color="#8FBC8F"))
            
        ext = self.format_menu.get().lower()
        quality = self.quality_var.get()
        
        yt_format = 'bestvideo+bestaudio/best'
        format_sort = None
        if quality == 'Audio Only':
            yt_format = 'bestaudio/best'
        elif quality != 'Best Quality':
            height = quality.replace('p', '')
            yt_format = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]/best'
            format_sort = [f'res:{height}']
            
        opts = {
            'outtmpl': f"{config.get('download_dir', 'Downloads')}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s",
            'format': yt_format,
            'merge_output_format': ext,
            'yes_playlist': True,
            'ignoreerrors': True  # Essential to skip private/deleted videos in playlists
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
