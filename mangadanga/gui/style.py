from tkinter import *
from tkinter import ttk


class GUIStyle:
    def __init__(self, master: Tk) -> None:
        self.master = master

    def set_style(self) -> None:
        self.master.configure(background="lavender")
        style = ttk.Style()
        self.set_labels_style(style)
        style.configure("TEntry", borderwidth=2, relief=RAISED)
        self.set_frames_style(style)
        self.set_button_style(style)
        self.set_notebook_style(style)
        self.set_combobox_style(style)

    def set_labels_style(self, style: ttk.Style) -> None:
        style.configure(
            "Title.TLabel",
            background="purple4",
            foreground="light goldenrod",
            font=("consolas", 15, "bold"),
            borderwidth=2,
            relief=RIDGE,
        )
        style.configure("Generic.TLabel", anchor=CENTER, font=("consolas", 8), background="lavender")

    def set_frames_style(self, style: ttk.Style) -> None:
        style.configure("TFrame", background="lavender")
        style.configure("TLabelframe", background="lavender", borderwidth=2, relief=GROOVE)
        style.configure("TLabelframe.Label", background="lavender", foreground="dark goldenrod", font=("consolas", 8))

    def set_button_style(self, style: ttk.Style) -> None:
        style.configure(
            "TButton",
            background="LavenderBlush3",
            borderwidth=3,
            font=("consolas", 7),
            anchor=CENTER,
            relief=GROOVE,
        )
        style.map(
            "TButton",
            background=[("pressed", "SlateBlue4"), ("active", "lavender blush")],
            foreground=[("pressed", "light goldenrod")],
            relief=[("pressed", SUNKEN)],
        )

    def set_notebook_style(self, style: ttk.Style) -> None:
        style.configure("TNotebook", background="lavender", borderwidth=1)
        style.configure(
            "TNotebook.Tab",
            background="lavender",
            font=("consolas", 8, "bold"),
            foreground="dark goldenrod",
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "SlateBlue4"), ("active", "lavender blush")],
            foreground=[("selected", "light goldenrod")],
        )

    def set_combobox_style(self, style: ttk.Style) -> None:
        style.configure("TCombobox", background="LavenderBlush3")
        style.map("TCombobox", background=[("active", "lavender blush")])
        self.master.option_add("*TCombobox*Listbox*Font", ("consolas", 8))
