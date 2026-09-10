import customtkinter as ctk
from backend.history import get_history, clear_history
import tkinter.messagebox as messagebox
from utils.logger_util import app_logger
import threading
import requests
from io import BytesIO
from PIL import Image

class DownloadManagerFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.header = ctk.CTkLabel(self, text="✎ Download History", font=ctk.CTkFont(family="Ink Free", size=36, weight="bold"), text_color="#8FBC8F")
        self.header.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=30)
        
        # History Panel (Left)
        self.history_frame = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color="#1E1C1A", border_width=2, border_color="#8FBC8F")
        self.history_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))
        
        hist_header_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        hist_header_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(hist_header_frame, text="✎ Download History", font=ctk.CTkFont(family="Ink Free", size=22, weight="bold"), text_color="#F5F5DC").pack(side="left", padx=10)
        self.clear_hist_btn = ctk.CTkButton(hist_header_frame, text="Clear History", width=110, height=35, corner_radius=15, fg_color="transparent", border_width=2, border_color="#F43F5E", text_color="#F43F5E", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=14, weight="bold"), command=self.do_clear_history)
        self.clear_hist_btn.pack(side="right", padx=10)

        self.history_container = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        self.history_container.pack(fill="both", expand=True)
        
        self.refresh()

    def do_clear_history(self):
        clear_history()
        self.refresh()

    def refresh(self):
        # Clear child widgets
        for widget in self.history_container.winfo_children():
            widget.destroy()
            
        history = get_history()
        if not history:
            ctk.CTkLabel(self.history_container, text="No offline history found.", font=ctk.CTkFont(family="Ink Free", size=16), text_color="gray50").pack(pady=40)
            return
            
        for item in history:
            card = ctk.CTkFrame(self.history_container, fg_color="transparent", border_width=1, border_color="#87CEEB", corner_radius=15)
            card.pack(fill="x", padx=10, pady=5)
            
            card.grid_columnconfigure(1, weight=1)
            card.grid_columnconfigure(2, weight=0)
            
            img_label = ctk.CTkLabel(card, text="✎ No Image", font=ctk.CTkFont(family="Ink Free", size=14), width=120, height=68, fg_color="#3E3C38", corner_radius=10)
            img_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
            
            ctk.CTkLabel(card, text=item.get("title", "Unknown"), font=ctk.CTkFont(family="Ink Free", size=16, weight="bold"), text_color="#F5F5DC", anchor="w", wraplength=250).grid(row=0, column=1, sticky="w", padx=10, pady=(10, 2))
            ctk.CTkLabel(card, text=f"URL: {item.get('url', '')[:30]}... | Date: {item.get('date', '')[:16]}", text_color="#87CEEB", font=ctk.CTkFont(family="Ink Free", size=12), anchor="w").grid(row=1, column=1, sticky="w", padx=10, pady=(0, 10))
            
            def open_dir(dl_item=item):
                import os
                from settings.config import config
                folder = config.get('download_dir', 'Downloads')
                os.makedirs(folder, exist_ok=True)
                # Try finding the exact file using title loosely
                title_frag = str(dl_item.get('title', ''))
                exact_path = None
                for fname in os.listdir(folder):
                    if title_frag in fname or fname.startswith(title_frag[:20]):
                        exact_path = os.path.join(folder, fname)
                        break
                
                try:
                    if exact_path and os.path.exists(exact_path):
                        # Open folder with file selected
                        import subprocess
                        subprocess.Popen(f'explorer /select,"{os.path.abspath(exact_path)}"')
                    else:
                        os.startfile(os.path.abspath(folder))
                except Exception:
                    os.startfile(os.path.abspath(folder))
                    
            btn = ctk.CTkButton(card, text="Open Folder", width=110, height=40, corner_radius=15, fg_color="transparent", border_width=2, border_color="#87CEEB", text_color="#87CEEB", hover_color="#5E4C38", font=ctk.CTkFont(family="Ink Free", size=14, weight="bold"), command=open_dir)
            btn.grid(row=0, column=2, rowspan=2, padx=15, pady=10)
            
            thumb_url = item.get("thumbnail")
            if thumb_url:
                def fetch_and_set_thumb(url_str, label_ref):
                    try:
                        resp = requests.get(url_str, timeout=5)
                        img = Image.open(BytesIO(resp.content))
                        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 68))
                        self.master.after(0, lambda: label_ref.configure(image=ctk_img, text=""))
                    except:
                        pass
                threading.Thread(target=fetch_and_set_thumb, args=(thumb_url, img_label), daemon=True).start()
