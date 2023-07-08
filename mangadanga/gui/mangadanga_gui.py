from tkinter import *
from tkinter import ttk

from .style import GUIStyle
from .widgets import GUIWidgets


class MangadangaGUI:
    def __init__(self, master: Tk, styles: GUIStyle, widgets: GUIWidgets) -> None:
        self.master = master
        self.styles = styles
        self.widgets = widgets
        self.set_gui()

    def set_gui(self) -> None:
        self.set_window()
        self.widgets.set_widgets()
        self.styles.set_style()

    def set_window(self) -> None:
        self.window_column_row_config()
        self.center_window()
        self.master.resizable(False, False)

    def window_column_row_config(self) -> None:
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=1)

    def center_window(self) -> None:
        window_width = 500
        window_height = 410
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_axis = int((screen_width / 2) - (window_width / 2))
        y_axis = int((screen_height / 2) - (window_height / 2)) - 70
        self.master.geometry(f"{window_width}x{window_height}+{x_axis}+{y_axis}")


# Tells Tk that if a user presses the Return key (Enter on Windows), it should call our mangadanga routine,
# the same as if they pressed the Start button.
# window.bind("<Return>", "same as 'command' value in the start button")


# def start() -> None:
#     url = url_entry.get()
#     chapter = [chapter_entry.get()]
#     chapter_range = (chapters_range_1_entry.get(), chapters_range_2_entry.get())
#     start_button.state(["disabled"]) if not url else start_button.state(["active"])
