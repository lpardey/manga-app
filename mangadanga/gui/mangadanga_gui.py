# Standard Library
import tkinter
import tkinter.ttk

# Local imports
from ..downloader.config import DownloaderConfig
from .style import GUIStyle
from .widgets import MainWindow


class MangadangaGUI:
    def __init__(self) -> None:
        self.container = tkinter.Tk()
        self.set_container_config()
        self.init_config = DownloaderConfig()
        self.widgets = MainWindow(self.container, self.init_config)
        self.styles = GUIStyle(self.container)

    def set_container_config(self) -> None:
        self.container.title("明るい")
        self.container.iconbitmap(
            r"C:\Users\lpard\repos\manga-app\mangadanga\gui\static\Guts.ico"
        )  # This is for windows
        self.container_column_row_config()
        self.center_container()
        self.container.resizable(False, False)

    def container_column_row_config(self) -> None:
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)
        self.container.rowconfigure(2, weight=1)

    def center_container(self) -> None:
        container_width = 500
        container_height = 410
        screen_width = self.container.winfo_screenwidth()
        screen_height = self.container.winfo_screenheight()
        x_axis = int((screen_width / 2) - (container_width / 2))
        y_axis = int((screen_height / 2) - (container_height / 2)) - 70
        self.container.geometry(f"{container_width}x{container_height}+{x_axis}+{y_axis}")
