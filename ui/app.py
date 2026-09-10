import customtkinter as ctk
import sys
import os
from PIL import Image, ImageTk
from ui.components import SidebarButton
from ui.home import HomeFrame
from ui.video_dl import VideoDownloaderFrame
from ui.playlist_dl import PlaylistDownloaderFrame
from ui.mp3_dl import MP3DownloaderFrame
from ui.download_manager import DownloadManagerFrame
from ui.settings import SettingsFrame
from ui.search import SearchFrame
from ui.logs import LogsFrame

class MediaYantraApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Media Yantra")
        def resource_path(relative_path):
            import sys, os
            try: return os.path.join(sys._MEIPASS, relative_path)
            except Exception: return os.path.join(os.path.abspath("."), relative_path)
        
        icon_path = resource_path(os.path.join("assets", "icon.ico"))
        try:
            self.iconbitmap(icon_path)
        except Exception:
            try:
                from PIL import Image, ImageTk
                img = ImageTk.PhotoImage(Image.open(icon_path))
                self.iconphoto(True, img)
            except Exception as e:
                pass
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#2b2b2b")
        
        # Configure layout (Grid: 1 row, 2 columns)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # ============ SIDEBAR ============
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1E1C1A")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="✎ Media Yantra", font=ctk.CTkFont(family="Ink Free", size=26, weight="bold"), text_color="#FFB347")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 30))
        
        self.sidebar_buttons = []
        
        self.home_btn = SidebarButton(self.sidebar_frame, text="⌂ Home", command=lambda: self.select_frame("home"))
        self.home_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        self.video_btn = SidebarButton(self.sidebar_frame, text="⯈ Video Downloader", command=lambda: self.select_frame("video"))
        self.video_btn.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.playlist_btn = SidebarButton(self.sidebar_frame, text="▤ Playlist Downloader", command=lambda: self.select_frame("playlist"))
        self.playlist_btn.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        self.audio_btn = SidebarButton(self.sidebar_frame, text="♫ Audio (MP3)", command=lambda: self.select_frame("audio"))
        self.audio_btn.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        self.downloads_btn = SidebarButton(self.sidebar_frame, text="⭳ Downloads", command=lambda: self.select_frame("downloads"))
        self.downloads_btn.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        
        self.settings_btn = SidebarButton(self.sidebar_frame, text="⛭ Settings", command=lambda: self.select_frame("settings"))
        self.settings_btn.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        self.logs_btn = SidebarButton(self.sidebar_frame, text="◧ Debug Logs", command=lambda: self.select_frame("logs"))
        self.logs_btn.grid(row=7, column=0, padx=10, pady=5, sticky="ew")
        
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        self.about_btn = SidebarButton(self.sidebar_frame, text="ℹ About", command=lambda: self.select_frame("about"))
        self.about_btn.grid(row=9, column=0, padx=10, pady=(5, 20), sticky="ew")
        
        # ============ MAIN CONTENT ============
        self.frames = {}
        
        self.home_frame = HomeFrame(self)
        self.frames["home"] = self.home_frame
        
        # Placeholder frames for others
        self.video_frame = VideoDownloaderFrame(self)
        self.frames["video"] = self.video_frame
        
        self.playlist_frame = PlaylistDownloaderFrame(self)
        self.frames["playlist"] = self.playlist_frame
        
        self.audio_frame = MP3DownloaderFrame(self)
        self.frames["audio"] = self.audio_frame
        
        self.downloads_frame = DownloadManagerFrame(self)
        self.frames["downloads"] = self.downloads_frame
        
        self.settings_frame = SettingsFrame(self)
        self.frames["settings"] = self.settings_frame
        
        self.logs_frame = LogsFrame(self)
        self.frames["logs"] = self.logs_frame
        
        self.about_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        try:
            abt_img = ctk.CTkImage(light_image=Image.open(resource_path(os.path.join("assets", "icon.ico"))), size=(130, 130))
            ctk.CTkLabel(self.about_frame, image=abt_img, text="").pack(pady=(60, 10))
            t_pad = 0
        except Exception:
            t_pad = 120
            
        ctk.CTkLabel(self.about_frame, text="✎ Media Yantra", font=ctk.CTkFont(family="Ink Free", size=42, weight="bold"), text_color="#FFB347").pack(pady=(t_pad, 10))
        ctk.CTkLabel(self.about_frame, text="Version 1.0.0", font=ctk.CTkFont(family="Ink Free", size=20), text_color="#F5F5DC").pack(pady=(0, 30))
        ctk.CTkLabel(self.about_frame, text="Hand-crafted By", font=ctk.CTkFont(family="Ink Free", size=18)).pack(pady=(0, 5))
        ctk.CTkLabel(self.about_frame, text="Kartik Kothalkar", font=ctk.CTkFont(family="Ink Free", size=28, weight="bold"), text_color="#8FBC8F").pack(pady=(0, 5))
        ctk.CTkLabel(self.about_frame, text="(Open Source Warrior)", font=ctk.CTkFont(family="Ink Free", size=18, slant="italic"), text_color="gray50").pack()
        self.frames["about"] = self.about_frame
        
        # Select default frame
        self.select_frame("home")

    def select_frame(self, name):
        # Update button colors
        buttons = {
            "home": self.home_btn,
            "video": self.video_btn,
            "playlist": self.playlist_btn,
            "audio": self.audio_btn,
            "downloads": self.downloads_btn,
            "settings": self.settings_btn,
            "logs": self.logs_btn,
            "about": self.about_btn,
        }
        
        for btn_name, btn in buttons.items():
            if btn_name == name:
                btn.configure(fg_color="#3E3C38")
            else:
                btn.configure(fg_color="transparent")
                
        # Show selected frame
        for frame_name, frame in self.frames.items():
            if frame_name == name:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()
