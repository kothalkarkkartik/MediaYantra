import customtkinter as ctk
from customtkinter import filedialog
from settings.config import config
import os

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.header = ctk.CTkLabel(self, text="✎ Settings", font=ctk.CTkFont(family="Ink Free", size=36, weight="bold"), text_color="#E6A8D7")
        self.header.pack(pady=(20, 30), anchor="w", padx=30)
        
        self.scroll = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#E6A8D7")
        self.scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        # General Settings
        # General Settings
        ctk.CTkLabel(self.scroll, text="✎ General", font=ctk.CTkFont(family="Ink Free", size=24, weight="bold", underline=True), text_color="#FFB347").pack(anchor="w", padx=20, pady=(20, 10))
        
        self.download_dir_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.download_dir_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.download_dir_frame, text="Download Folder:", font=ctk.CTkFont(family="Ink Free", size=18), text_color="#F5F5DC", width=150, anchor="w").pack(side="left")
        self.dir_entry = ctk.CTkEntry(self.download_dir_frame, width=300, font=ctk.CTkFont(family="Ink Free", size=16), corner_radius=10, fg_color="#3E3C38", border_color="#87CEEB")
        self.dir_entry.pack(side="left", padx=10)
        self.dir_entry.insert(0, config.get("download_dir", ""))
        
        self.browse_btn = ctk.CTkButton(self.download_dir_frame, text="Browse", width=90, height=35, corner_radius=15, fg_color="transparent", border_width=2, border_color="#87CEEB", text_color="#87CEEB", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=16, weight="bold"), command=self.do_browse)
        self.browse_btn.pack(side="left")
        
        # Network Settings
        # Network Settings
        ctk.CTkLabel(self.scroll, text="✎ Network & Queue", font=ctk.CTkFont(family="Ink Free", size=24, weight="bold", underline=True), text_color="#87CEEB").pack(anchor="w", padx=20, pady=(20, 10))
        
        self.concurrent_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.concurrent_frame.pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(self.concurrent_frame, text="Concurrent Downloads:", font=ctk.CTkFont(family="Ink Free", size=18), text_color="#F5F5DC", width=150, anchor="w").pack(side="left")
        self.concurrent_menu = ctk.CTkOptionMenu(self.concurrent_frame, values=["1", "2", "3", "4", "5", "8", "10"], font=ctk.CTkFont(family="Ink Free", size=16), corner_radius=10, fg_color="#3E3C38", button_color="#5E4C38")
        self.concurrent_menu.pack(side="left", padx=10)
        self.concurrent_menu.set(str(config.get("concurrent_downloads", 3)))
        
        # Advanced Settings
        # Advanced Settings
        ctk.CTkLabel(self.scroll, text="✎ Advanced API Config", font=ctk.CTkFont(family="Ink Free", size=24, weight="bold", underline=True), text_color="#8FBC8F").pack(anchor="w", padx=20, pady=(20, 10))
        
        self.cookies_frame = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.cookies_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(self.cookies_frame, text="Import Cookies From:", font=ctk.CTkFont(family="Ink Free", size=18), text_color="#F5F5DC", width=150, anchor="w").pack(side="left")
        self.cookies_menu = ctk.CTkOptionMenu(self.cookies_frame, values=["None", "Chrome", "Edge", "Firefox", "Opera", "Brave", "Safari"], font=ctk.CTkFont(family="Ink Free", size=16), corner_radius=10, fg_color="#3E3C38", button_color="#5E4C38")
        self.cookies_menu.pack(side="left", padx=10)
        self.cookies_menu.set(config.get("cookies_browser", "None"))
        
        # Save mechanism
        self.status_lbl = ctk.CTkLabel(self.scroll, text="", font=ctk.CTkFont(family="Ink Free", size=16, weight="bold"), text_color="#8FBC8F")
        self.status_lbl.pack(anchor="e", padx=20, pady=(20, 0))
        
        self.save_btn = ctk.CTkButton(self.scroll, text="Save Settings", height=55, corner_radius=15, fg_color="transparent", border_width=2, border_color="#8FBC8F", text_color="#8FBC8F", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=20, weight="bold"), command=self.save_settings)
        self.save_btn.pack(anchor="e", padx=20, pady=(5, 40))

    def do_browse(self):
        folder = filedialog.askdirectory(title="Select Download Directory")
        if folder:
            self.dir_entry.delete(0, "end")
            self.dir_entry.insert(0, os.path.normpath(folder))

    def save_settings(self):
        new_dir = self.dir_entry.get().strip()
        new_concurrent = int(self.concurrent_menu.get())
        new_cookies = self.cookies_menu.get()
        
        config.set("download_dir", new_dir)
        config.set("concurrent_downloads", new_concurrent)
        config.set("cookies_browser", new_cookies)
        
        os.makedirs(new_dir, exist_ok=True)
        
        self.status_lbl.configure(text="Settings successfully reloaded across all modules!")
        self.master.after(3000, lambda: self.status_lbl.configure(text=""))
