# Standard Library
import tkinter
from tkinter import ttk


class GUIStyle:
    def __init__(self, container: tkinter.Tk) -> None:
        self.container = container
        self.style = ttk.Style()
        self.set_style()

    def set_style(self) -> None:
        self.container.configure(background="lavender")
        self.set_labels_style()
        self.style.configure("TEntry", borderwidth=2, relief=tkinter.RAISED)
        self.set_frames_style()
        self.set_button_style()
        self.set_notebook_style()
        self.set_combobox_style()

    def set_labels_style(self) -> None:
        self.style.configure(
            "TopBanner.TLabel",
            background="purple4",
            foreground="light goldenrod",
            font=("consolas", 15, "bold"),
            borderwidth=2,
            relief=tkinter.RIDGE,
        )
        self.style.configure(
            "Generic.TLabel",
            anchor=tkinter.CENTER,
            font=("consolas", 10),
            background="lavender",
        )

    def set_frames_style(self) -> None:
        self.style.configure("TFrame", background="lavender")
        self.style.configure("TLabelframe", background="lavender", borderwidth=2, relief=tkinter.GROOVE)
        self.style.configure(
            "TLabelframe.Label",
            background="lavender",
            foreground="dark goldenrod",
            font=("consolas", 10),
        )

    def set_button_style(self) -> None:
        self.style.configure(
            "TButton",
            background="LavenderBlush3",
            borderwidth=3,
            font=("consolas", 9),
            anchor=tkinter.CENTER,
            relief=tkinter.GROOVE,
        )
        self.style.map(
            "TButton",
            background=[("pressed", "SlateBlue4"), ("active", "lavender blush")],
            foreground=[("pressed", "light goldenrod")],
            relief=[("pressed", tkinter.SUNKEN)],
        )

    def set_notebook_style(self) -> None:
        self.style.configure("TNotebook", background="lavender", borderwidth=1)
        self.style.configure(
            "TNotebook.Tab",
            background="lavender",
            font=("consolas", 10, "bold"),
            foreground="dark goldenrod",
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", "SlateBlue4"), ("active", "lavender blush")],
            foreground=[("selected", "light goldenrod")],
        )

    def set_combobox_style(self) -> None:
        self.style.configure("TCombobox", background="LavenderBlush3")
        self.style.map("TCombobox", background=[("active", "lavender blush")])
        self.container.option_add("*TCombobox*Listbox*Font", ("consolas", 10))
