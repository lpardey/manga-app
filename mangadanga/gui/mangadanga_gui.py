# Standard Library
import tkinter
import tkinter.ttk

# Local imports
from ..downloader.config import DownloaderConfig
from .style import GUIStyle
from .widgets import MainWindow


class MangadangaGUI:
    def __init__(self) -> None:
        self.container = self.set_container()
        self.init_config = DownloaderConfig()
        self.widgets = MainWindow(self.container, self.init_config)
        self.styles = GUIStyle(self.container)

    def set_container(self) -> tkinter.Tk:
        container = tkinter.Tk()
        container.title("明るい")
        container.iconbitmap(r"C:\Users\lpard\repos\manga-app\mangadanga\gui\static\Guts.ico")  # This is for windows
        self.main_window_column_row_config()
        self.center_main_window()
        container.resizable(False, False)
        return container

    def main_window_column_row_config(self) -> None:
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)
        self.container.rowconfigure(2, weight=1)

    def center_main_window(self) -> None:
        main_window_width = 500
        main_window_height = 410
        screen_width = self.container.winfo_screenwidth()
        screen_height = self.container.winfo_screenheight()
        x_axis = int((screen_width / 2) - (main_window_width / 2))
        y_axis = int((screen_height / 2) - (main_window_height / 2)) - 70
        self.container.geometry(f"{main_window_width}x{main_window_height}+{x_axis}+{y_axis}")
