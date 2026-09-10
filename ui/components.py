import customtkinter as ctk

class SidebarButton(ctk.CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(
            master=master,
            text=text,
            command=command,
            corner_radius=20,
            height=45,
            border_spacing=10,
            text_color="#F5F5DC",
            hover_color="#3E3C38",
            anchor="w",
            font=ctk.CTkFont(family="Ink Free", size=18, weight="bold"),
            fg_color="transparent",
            **kwargs
        )
