import customtkinter as ctk

class SidebarButton(ctk.CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(
            master=master,
            text=text,
            command=command,
            corner_radius=8,
            height=40,
            border_spacing=10,
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            **kwargs
        )
