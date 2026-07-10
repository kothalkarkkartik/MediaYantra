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

        self.title = ctk.CTkLabel(main_container, text="◈ Media Yantra ◈", font=ctk.CTkFont(size=42, weight="bold"), text_color="#E2E8F0")
        self.title.pack(pady=(50, 10))
        
        self.subtitle = ctk.CTkLabel(main_container, text="⮞ The streamlined media downloader", font=ctk.CTkFont(size=20), text_color="#94A3B8")
        self.subtitle.pack(pady=(0, 40))
        
        self.url_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        self.url_frame.pack(fill="x", padx=40, pady=20)
        
        self.url_entry = ctk.CTkEntry(self.url_frame, placeholder_text="⎘ Paste your video or playlist URL here...", height=55, font=ctk.CTkFont(size=16), corner_radius=8, border_width=1, border_color="#475569", fg_color="#1E293B")
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.paste_btn = ctk.CTkButton(self.url_frame, text="↳ Paste", width=90, height=55, corner_radius=8, fg_color="#334155", hover_color="#475569", font=ctk.CTkFont(weight="bold"))
        self.paste_btn.pack(side="left", padx=5)
        
        self.analyze_btn = ctk.CTkButton(self.url_frame, text="► Analyze", width=140, height=55, corner_radius=8, fg_color="#475569", hover_color="#64748B", text_color="white", font=ctk.CTkFont(size=15, weight="bold"), command=self.analyze_url)
        self.analyze_btn.pack(side="left", padx=5)
        
        self.clear_btn = ctk.CTkButton(self.url_frame, text="✖ Clear", width=90, height=55, corner_radius=8, fg_color="#334155", hover_color="#475569", font=ctk.CTkFont(weight="bold"), command=lambda: self.url_entry.delete(0, 'end'))
        self.clear_btn.pack(side="left", padx=5)
        
        self.cards_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        self.cards_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        self.cards_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        feat_1 = ctk.CTkFrame(self.cards_frame, corner_radius=10, fg_color="#1E293B", border_width=0)
        feat_1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(feat_1, text="⯈", font=ctk.CTkFont(size=36), text_color="#E2E8F0").pack(pady=(20,5))
        ctk.CTkLabel(feat_1, text="Videos", font=ctk.CTkFont(weight="bold", size=15)).pack()
        ctk.CTkLabel(feat_1, text="High quality extraction", text_color="gray50", wraplength=120).pack(pady=(5,20))

        feat_2 = ctk.CTkFrame(self.cards_frame, corner_radius=10, fg_color="#1E293B", border_width=0)
        feat_2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(feat_2, text="♫", font=ctk.CTkFont(size=36), text_color="#E2E8F0").pack(pady=(20,5))
        ctk.CTkLabel(feat_2, text="Audio & MP3", font=ctk.CTkFont(weight="bold", size=15)).pack()
        ctk.CTkLabel(feat_2, text="Lossless sound profiles", text_color="gray50", wraplength=120).pack(pady=(5,20))

        feat_3 = ctk.CTkFrame(self.cards_frame, corner_radius=10, fg_color="#1E293B", border_width=0)
        feat_3.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(feat_3, text="▤", font=ctk.CTkFont(size=36), text_color="#E2E8F0").pack(pady=(20,5))
        ctk.CTkLabel(feat_3, text="Playlists", font=ctk.CTkFont(weight="bold", size=15)).pack()
        ctk.CTkLabel(feat_3, text="Automated batch queues", text_color="gray50", wraplength=120).pack(pady=(5,20))

        feat_4 = ctk.CTkFrame(self.cards_frame, corner_radius=10, fg_color="#1E293B", border_width=0)
        feat_4.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(feat_4, text="⮞", font=ctk.CTkFont(size=36), text_color="#E2E8F0").pack(pady=(20,5))
        ctk.CTkLabel(feat_4, text="Hyper-Fast", font=ctk.CTkFont(weight="bold", size=15)).pack()
        ctk.CTkLabel(feat_4, text="Multi-threaded pipelines", text_color="gray50", wraplength=120).pack(pady=(5,20))
        
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
