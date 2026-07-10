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
        self.grid_columnconfigure(1, weight=1)
        
        self.header = ctk.CTkLabel(self, text="⭳ History & Logs", font=ctk.CTkFont(size=28, weight="bold"), text_color="#A855F7")
        self.header.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="w", padx=30)
        
        # History Panel (Left)
        self.history_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.history_frame.grid(row=1, column=0, sticky="nsew", padx=(30, 10), pady=(0, 20))
        
        hist_header_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        hist_header_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(hist_header_frame, text="Download History", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        self.clear_hist_btn = ctk.CTkButton(hist_header_frame, text="Clear History", width=100, height=28, fg_color="#F43F5E", hover_color="#E11D48", command=self.do_clear_history)
        self.clear_hist_btn.pack(side="right")

        self.history_container = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        self.history_container.pack(fill="both", expand=True)
        
        # Logs Panel (Right)
        self.logs_frame = ctk.CTkScrollableFrame(self, corner_radius=10, fg_color="#1E293B")
        self.logs_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 30), pady=(0, 20))
        
        logs_header_frame = ctk.CTkFrame(self.logs_frame, fg_color="transparent")
        logs_header_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(logs_header_frame, text="Application Logs", font=ctk.CTkFont(size=18, weight="bold"), text_color="white").pack(side="left", padx=5)
        self.clear_logs_btn = ctk.CTkButton(logs_header_frame, text="Clear Logs", width=100, height=28, fg_color="#F43F5E", hover_color="#E11D48", command=self.do_clear_logs)
        self.clear_logs_btn.pack(side="right", padx=5)
        self.log_text = ctk.CTkTextbox(self.logs_frame, fg_color="transparent", text_color="#A7F3D0", wrap="word", state="normal")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_text.configure(state="disabled")
        
        # Connect to logger
        app_logger.register_callback(self._on_new_log)
        for log in reversed(app_logger.logs):
            self._on_new_log(log)
            
        self.refresh()

    def _on_new_log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("0.0", msg + "\n")
        self.log_text.configure(state="disabled")

    def do_clear_history(self):
        clear_history()
        self.refresh()
        
    def do_clear_logs(self):
        app_logger.clear()
        self.log_text.configure(state="normal")
        self.log_text.delete("0.0", "end")
        self.log_text.configure(state="disabled")

    def refresh(self):
        # Clear child widgets
        for widget in self.history_container.winfo_children():
            widget.destroy()
            
        history = get_history()
        if not history:
            ctk.CTkLabel(self.history_container, text="No offline history found.", text_color="gray50").pack(pady=40)
            return
            
        for item in history:
            card = ctk.CTkFrame(self.history_container, fg_color="#334155", corner_radius=8)
            card.pack(fill="x", padx=10, pady=5)
            
            card.grid_columnconfigure(1, weight=1)
            card.grid_columnconfigure(2, weight=0)
            
            img_label = ctk.CTkLabel(card, text="No Image", width=120, height=68, fg_color="gray20", corner_radius=5)
            img_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
            
            ctk.CTkLabel(card, text=item.get("title", "Unknown"), font=ctk.CTkFont(weight="bold"), anchor="w", wraplength=250).grid(row=0, column=1, sticky="w", padx=10, pady=(10, 2))
            ctk.CTkLabel(card, text=f"URL: {item.get('url', '')[:30]}... | Date: {item.get('date', '')[:16]}", text_color="#94A3B8", font=("Arial", 10), anchor="w").grid(row=1, column=1, sticky="w", padx=10, pady=(0, 10))
            
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
                    
            btn = ctk.CTkButton(card, text="Open Folder", width=100, height=35, fg_color="#3B82F6", hover_color="#2563EB", command=open_dir)
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
