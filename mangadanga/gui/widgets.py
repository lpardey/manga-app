import asyncio
import tkinter
from tkinter import Misc, ttk, filedialog, messagebox
from mangadanga.downloader import downloader_factory, DownloaderConfig
from typing import Callable
import logging
from ..downloader.config import ChapterStrategyConfig
from ..downloader.exceptions import DownloaderException
from .utils import validate_non_empty, validate_numeric
from concurrent import futures

logger = logging.getLogger("MangaDanga-GUI")

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


class MainWindow:
    def __init__(self, container: Misc, init_config: DownloaderConfig) -> None:
        self.init_config = init_config
        self.top_banner = TopBanner(container)
        self.main_tabs = NotebookComponent(container, init_config)
        self.download_button = DownloadButton(container, self.get_config)
        self.window_general_management(container)

    def get_config(self) -> DownloaderConfig:
        url = self.main_tabs.download_tab.url_component.url_value.get()
        validate_non_empty(url, "'URL'")
        path = self.main_tabs.download_tab.local_path_component.path_value.get()
        validate_non_empty(path, "'Save to'")
        raw_threads = self.main_tabs.settings_tab.multithreading.combo_box.get()
        validate_non_empty(raw_threads, "'Threads'")
        validate_numeric(raw_threads, "'Threads'")
        threads = int(raw_threads)
        chapter_strategy_config = self.main_tabs.settings_tab.download_management.get_chapter_selection_strategy()
        config = DownloaderConfig(url=url, path=path, chapter_strategy=chapter_strategy_config, threads=threads)
        return config

    def window_general_management(self, container: Misc) -> None:
        container.bind("<Escape>", lambda e: self.quit(container))
        container.protocol("WM_DELETE_WINDOW", lambda: self.quit(container))

    @staticmethod
    def quit(container: Misc) -> None:
        exit = messagebox.askyesno(title="Exit", message="Do you want to exit MangaDanga?")
        if exit:
            container.destroy()


class TopBanner:
    def __init__(self, container: Misc) -> None:
        self.label = ttk.Label(
            container,
            text="MangaDanga",
            anchor=tkinter.CENTER,
            style="TopBanner.TLabel",
        )
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.NSEW)


class NotebookComponent:
    def __init__(self, container: Misc, init_config: DownloaderConfig) -> None:
        self.notebook = ttk.Notebook(container, style="TNotebook")
        self.notebook.grid(row=1, column=0)
        self.download_tab = DownloadTab(self.notebook, init_config)
        self.settings_tab = SettingsTab(self.notebook, init_config)


class DownloadButton:
    def __init__(self, container: Misc, get_config: Callable) -> None:
        self.container = container
        self.button = ttk.Button(
            container,
            text="Download",
            command=self.handle_download_button,
            width=15,
            style="TButton",
        )
        self.button.grid(row=2, column=0, ipady=1, padx=10, pady=10)
        self.get_config = get_config
        self.button.bind("<Return>", lambda e: self.handle_download_button())

    def handle_download_button(self) -> None:
        try:
            config = self.get_config()
            downloader = downloader_factory(config)
            asyncio.run(downloader.download())
            messagebox.showinfo(title="MangaDanga", message="Mandanga completed!")
        except DownloaderException as e:
            logger.exception(e)
            messagebox.showwarning(title="Warning!", message=e)
        except Exception as e:
            logger.exception(e)
            messagebox.showerror(title="Error!", message=f"Something unexpected happened: {e}")


class DownloadTab:
    def __init__(self, container: ttk.Notebook, init_config: DownloaderConfig) -> None:
        self.frame = ttk.Frame(container, style="TFrame")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        container.add(self.frame, text="Download")

        self.url_component = UrlComponent(self.frame)
        self.local_path_component = LocalPathComponent(self.frame, init_config)


class UrlComponent:
    def __init__(self, container: Misc) -> None:
        self.label_frame = ttk.Labelframe(container, text="URL", style="TLabelframe")
        self.label_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tkinter.EW)

        self.url_value = tkinter.StringVar()
        self.text = ttk.Entry(
            self.label_frame,
            textvariable=self.url_value,
            width=50,
            font=("consolas", 8),
            style="TEntry",
        )
        self.text.grid(row=0, column=0, columnspan=2, ipady=2, padx=10, pady=10, sticky=tkinter.EW)
        self.text.focus()


class LocalPathComponent:
    def __init__(self, container: Misc, init_config: DownloaderConfig) -> None:
        self.init_config = init_config
        self.label_frame = ttk.Labelframe(container, text="Save to", style="TLabelframe")
        self.label_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NEW")
        self.path_value = tkinter.StringVar(value=self.init_config.path)
        self.text = ttk.Entry(
            self.label_frame, textvariable=self.path_value, width=36, font=("consolas", 8), style="TEntry"
        )
        self.text.grid(row=1, column=0, ipady=2, padx=10, pady=10, sticky="NEW")
        self.button = ttk.Button(
            self.label_frame,
            text="Browse",
            command=self.handle_browse_button,
            width=9,
            style="TButton",
        )
        self.button.grid(row=1, column=1, ipady=1, padx=10, pady=10)
        self.button.bind("<Return>", lambda e: self.handle_browse_button())

    def handle_browse_button(self) -> None:
        try:
            save_to_path = filedialog.askdirectory(initialdir=self.init_config.path)
            validate_non_empty(field=save_to_path, name="'Save to'")
        except DownloaderException as e:
            logger.exception(e)
            messagebox.showwarning(title="Warning!", message=e)
        except Exception as e:
            logger.exception(e)
            messagebox.showerror(title="Error!", message=f"Something unexpected happened: {e}")
        self.path_value.set(save_to_path)


class SettingsTab:
    def __init__(self, container: ttk.Notebook, init_config: DownloaderConfig) -> None:
        self.frame = ttk.Frame(container, style="TFrame")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        container.add(self.frame, text="Settings")

        self.download_management = DownloadManagementComponent(self.frame)
        self.multithreading = MultithreadingComponent(self.frame, init_config)


class DownloadManagementComponent:
    def __init__(self, container: Misc) -> None:
        self.label_frame = ttk.Labelframe(container, text="Download Management", style="TLabelframe")
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky=tkinter.EW)

        self.chapter_list_input = tkinter.StringVar()
        self.chapter_range_lower_bound_input = tkinter.StringVar()
        self.chapter_range_upper_bound_input = tkinter.StringVar()
        self.radio_input = tkinter.IntVar()
        self.set_radiobuttons()

        self.set_chapters_entry()

        self.set_chapter_range_entry_lower_bound()
        self.set_chapter_range_separator_label()
        self.set_chapter_range_entry_upper_bound()

    def set_radiobuttons(self) -> None:
        chapter_options = ["All chapters", "Chapter/s", "Chapter range"]
        for index, text in enumerate(chapter_options):
            radiobutton = tkinter.Radiobutton(
                self.label_frame,
                text=text,
                variable=self.radio_input,
                value=index,
                font=("consolas", 8),
                background="lavender",
                activebackground="lavender",
                highlightthickness=0,
            )
            radiobutton.grid(row=index, column=0, padx=10, pady=10, sticky=tkinter.W)

    def set_chapters_entry(self) -> None:
        self.chapter_list_input = tkinter.StringVar()
        chapter_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_list_input,
            width=10,
            font=("consolas", 8),
            style="TEntry",
        )
        chapter_entry.grid(row=1, column=2, columnspan=3, ipady=2, padx=10, pady=10, sticky=tkinter.EW)

    def set_chapter_range_entry_lower_bound(self) -> None:
        self.chapter_range_lower_bound_input = tkinter.StringVar()
        chapter_r1_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_range_lower_bound_input,
            width=3,
            font=("consolas", 8),
            style="TEntry",
        )
        chapter_r1_entry.grid(row=2, column=2, ipady=2, padx=10, pady=10, sticky=tkinter.EW)

    def set_chapter_range_separator_label(self) -> None:
        self.separator_label = ttk.Label(self.label_frame, text="To", anchor=tkinter.CENTER, style="Generic.TLabel")
        self.separator_label.grid(row=2, column=3, padx=10, pady=10)

    def set_chapter_range_entry_upper_bound(self) -> None:
        self.chapter_range_upper_bound_input = tkinter.StringVar()
        chapter_r2_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_range_upper_bound_input,
            width=3,
            font=("consolas", 8),
            style="TEntry",
        )
        chapter_r2_entry.grid(row=2, column=4, ipady=2, padx=10, pady=10, sticky=tkinter.EW)

    def get_chapter_selection_strategy(self) -> ChapterStrategyConfig:
        strategies = {0: "all", 1: "list", 2: "range"}
        config = ChapterStrategyConfig()
        config.strategy = strategies[self.radio_input.get()]
        match config.strategy:
            case "list":
                chapters = self.get_chapters_list()
                config.config = {"chapters": chapters}
            case "range":
                lower_bound, upper_bound = self.get_chapter_range_bounds()
                config.config = {"lower_bound": lower_bound, "upper_bound": upper_bound}
            case _:
                pass
        return config

    def get_chapters_list(self) -> list[str]:
        raw_chapters = self.chapter_list_input.get().strip().replace(" ", ",")
        validate_non_empty(raw_chapters, "Chapter/s")
        chapters_list = raw_chapters.split(",")
        clean_chapters = [chapter for chapter in chapters_list if chapter]
        return clean_chapters

    def get_chapter_range_bounds(self) -> tuple[str, str]:
        raw_lower = self.chapter_range_lower_bound_input.get().strip()
        clean_lower = self.proccess_range_bound(raw_lower)
        raw_upper = self.chapter_range_upper_bound_input.get().strip()
        clean_upper = self.proccess_range_bound(raw_upper)
        return clean_lower, clean_upper

    @staticmethod
    def proccess_range_bound(raw_bound: str) -> str:
        raw_bound = raw_bound.strip()
        validate_non_empty(raw_bound, "'Chapter range bound'")
        validate_numeric(raw_bound, "'Chapter range bound'")
        return raw_bound


class MultithreadingComponent:
    def __init__(self, container: Misc, init_config: DownloaderConfig) -> None:
        self.label_frame = ttk.Labelframe(container, text="Multithreading", style="TLabelframe")
        self.label_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky=tkinter.EW)

        self.label_frame.columnconfigure(0)
        self.label_frame.columnconfigure(1)

        self.label = ttk.Label(self.label_frame, text="Number of threads:", style="Generic.TLabel")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.W)

        self.combo_box = ttk.Combobox(self.label_frame, values=list(range(1, 11)), width=3, font=("consolas", 8))
        self.combo_box.set(init_config.threads)
        self.combo_box.grid(row=0, column=1, ipady=2, padx=10, pady=10)
