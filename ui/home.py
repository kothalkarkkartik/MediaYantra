import customtkinter as ctk
from PIL import Image
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HomeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)

        self.title = ctk.CTkLabel(main_container, text="✎ Media Yantra", font=ctk.CTkFont(family="Ink Free", size=48, weight="bold"), text_color="#F5F5DC")
        self.title.pack(pady=(50, 10))
        
        self.subtitle = ctk.CTkLabel(main_container, text="Hand-crafted media downloader", font=ctk.CTkFont(family="Ink Free", size=22, slant="italic"), text_color="#D1D5DB")
        self.subtitle.pack(pady=(0, 40))
        
        self.url_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        self.url_frame.pack(fill="x", padx=40, pady=20)
        
        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="✎ Paste your video or playlist URL here...", height=55, font=ctk.CTkFont(family="Ink Free", size=18), corner_radius=15, border_width=2, border_color="#F5F5DC", fg_color="#3E3C38", text_color="#F5F5DC", placeholder_text_color="#A3A3A3")
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.paste_btn = ctk.CTkButton(self.url_frame, text="Paste", width=90, height=55, corner_radius=15, fg_color="transparent", hover_color="#5E4C38", border_width=2, border_color="#FFB347", text_color="#FFB347", font=ctk.CTkFont(family="Ink Free", size=18, weight="bold"))
        self.paste_btn.pack(side="left", padx=5)
        
        self.analyze_btn = ctk.CTkButton(self.url_frame, text="Analyze", width=140, height=55, corner_radius=15, fg_color="transparent", hover_color="#5E4C38", border_width=2, border_color="#8FBC8F", text_color="#8FBC8F", font=ctk.CTkFont(family="Ink Free", size=18, weight="bold"), command=self.analyze_url)
        self.analyze_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(self.url_frame, text="Clear", width=90, height=55, corner_radius=15, fg_color="transparent", hover_color="#5E4C38", border_width=2, border_color="#E6A8D7", text_color="#E6A8D7", font=ctk.CTkFont(family="Ink Free", size=18, weight="bold"), command=lambda: self.url_entry.delete(0, 'end'))
        self.clear_btn.pack(side="left", padx=5)
        
        self.cards_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.cards_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        feat_1 = ctk.CTkFrame(self.cards_frame, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#8FBC8F")
        feat_1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(feat_1, text="▶", font=ctk.CTkFont(size=42), text_color="#F5F5DC").pack(pady=(20,5))
        ctk.CTkLabel(feat_1, text="Videos", font=ctk.CTkFont(family="Ink Free", weight="bold", size=18), text_color="#8FBC8F").pack()
        ctk.CTkLabel(feat_1, text="High quality extraction", font=ctk.CTkFont(family="Ink Free", size=14), text_color="#D1D5DB", wraplength=120).pack(pady=(5,20))

        feat_2 = ctk.CTkFrame(self.cards_frame, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#FFB347")
        feat_2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(feat_2, text="♪", font=ctk.CTkFont(size=42), text_color="#F5F5DC").pack(pady=(20,5))
        ctk.CTkLabel(feat_2, text="Audio & MP3", font=ctk.CTkFont(family="Ink Free", weight="bold", size=18), text_color="#FFB347").pack()
        ctk.CTkLabel(feat_2, text="Lossless sound profiles", font=ctk.CTkFont(family="Ink Free", size=14), text_color="#D1D5DB", wraplength=120).pack(pady=(5,20))

        feat_3 = ctk.CTkFrame(self.cards_frame, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#E6A8D7")
        feat_3.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(feat_3, text="☰", font=ctk.CTkFont(size=42), text_color="#F5F5DC").pack(pady=(20,5))
        ctk.CTkLabel(feat_3, text="Playlists", font=ctk.CTkFont(family="Ink Free", weight="bold", size=18), text_color="#E6A8D7").pack()
        ctk.CTkLabel(feat_3, text="Automated batch queues", font=ctk.CTkFont(family="Ink Free", size=14), text_color="#D1D5DB", wraplength=120).pack(pady=(5,20))

        feat_4 = ctk.CTkFrame(self.cards_frame, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#87CEEB")
        feat_4.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(feat_4, text="⚡", font=ctk.CTkFont(size=42), text_color="#F5F5DC").pack(pady=(20,5))
        ctk.CTkLabel(feat_4, text="Hyper-Fast", font=ctk.CTkFont(family="Ink Free", weight="bold", size=18), text_color="#87CEEB").pack()
        ctk.CTkLabel(feat_4, text="Multi-threaded pipelines", font=ctk.CTkFont(family="Ink Free", size=14), text_color="#D1D5DB", wraplength=120).pack(pady=(5,20))
        
        self.disclaimer_label = ctk.CTkLabel(main_container, text="⯎ Please ensure all downloading functionality respects the terms of service of source platforms.\nOnly download content where it is explicitly authorized by the creator or copyright holder.", font=ctk.CTkFont(size=12, slant="italic"), text_color="gray50")
        self.disclaimer_label.pack(side="bottom", pady=20)
        
        self.paste_btn.configure(command=self.paste_url)

    def paste_url(self):
        try:
            url = self.master.clipboard_get()
            self.url_entry.delete(0, 'end')
            self.url_entry.insert(0, url)
        except:
            pass
            
    def analyze_url(self):
        url = self.url_entry.get().strip()
        if not url: return
        if "playlist" in url.lower():
            self.master.select_frame("playlist")
            self.master.frames["playlist"].url_entry.delete(0, 'end')
            self.master.frames["playlist"].url_entry.insert(0, url)
        else:
            self.master.select_frame("video")
            self.master.frames["video"].url_entry.delete(0, 'end')
            self.master.frames["video"].url_entry.insert(0, url)
            self.master.frames["video"].fetch_metadata()
