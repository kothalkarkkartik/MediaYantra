import customtkinter as ctk

class SearchFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.header = ctk.CTkLabel(self, text="Search YouTube", font=ctk.CTkFont(size=28, weight="bold"), text_color="#A855F7")
        self.header.pack(pady=(20, 10), anchor="w", padx=30)
        
        self.search_bar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_bar_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self.search_entry = ctk.CTkEntry(self.search_bar_frame, placeholder_text="Search query...", height=40, corner_radius=8)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.search_btn = ctk.CTkButton(self.search_bar_frame, text="Search", height=40, width=120)
        self.search_btn.pack(side="left")
        
        self.results_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.results_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        ctk.CTkLabel(self.results_frame, text="Search results will appear here.", text_color="gray50").pack(pady=40)
