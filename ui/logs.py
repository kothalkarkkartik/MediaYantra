import customtkinter as ctk
from utils.logger_util import app_logger

class LogsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Application Logs", font=ctk.CTkFont(size=28, weight="bold"), text_color="#A855F7")
        self.header.grid(row=0, column=0, pady=(20, 10), sticky="w", padx=30)
        
        # Log Textbox
        self.log_box = ctk.CTkTextbox(self, corner_radius=10, fg_color=("gray85", "gray15"), font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))
        
        # Clear Button
        self.clear_btn = ctk.CTkButton(self, text="Clear Logs", fg_color="#EF4444", hover_color="#DC2626", command=self.clear_logs)
        self.clear_btn.grid(row=2, column=0, sticky="e", padx=30, pady=(0, 20))
        
        # Load initial logs backwards since logger_util adds to start of list
        for entry in reversed(app_logger.logs):
            self._append_log_text(entry)
            
        # Register callback for new logs
        app_logger.register_callback(self.add_log_entry)

    def _append_log_text(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def add_log_entry(self, entry):
        # Must be thread-safe for CustomTkinter
        self.master.after(0, lambda: self._append_log_text(entry))

    def clear_logs(self):
        app_logger.clear()
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
