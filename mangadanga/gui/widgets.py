from __future__ import annotations

# Standard Library
import asyncio
import logging
import threading
import tkinter
from tkinter import Misc, filedialog, messagebox, ttk
from typing import Any, Callable, Coroutine, Literal

# From apps
from mangadanga.downloader import DownloaderConfig, downloader_factory

# Local imports
from ..downloader.config import ChapterStrategyConfig
from ..downloader.exceptions import DownloaderException
from .events import (
    EVENT_MANAGER,
    EventManager,
    OnChapterDownloadFinished,
    OnCloseProgress,
    OnDownloadFinished,
    OnDownloadFinishedGUI,
    OnMangaInfoUpdate,
    OnQuit,
    OnStartDownload,
)
from .utils import validate_non_empty, validate_numeric

logger = logging.getLogger("MangaDanga-GUI")


class MainWindow:
    def __init__(
        self,
        container: tkinter.Tk,
        init_config: DownloaderConfig,
    ) -> None:
        self.container = container
        self.init_config = init_config
        self.event_manager = EVENT_MANAGER
        self.top_banner = TopBanner(self.container)
        self.main_tabs = NotebookComponent(self.container, self.init_config)
        self.download_button = DownloadButton(self.container, self.get_config, self.event_manager)
        self.task_process_event_queue()
        self.set_events()

    def get_config(self) -> DownloaderConfig:
        url = self.main_tabs.download_tab.url_component.get_url()
        path = self.main_tabs.download_tab.local_path_component.get_path()
        chapter_strategy_config = self.main_tabs.settings_tab.download_management.get_chapter_selection_strategy()
        threads = self.main_tabs.settings_tab.multithreading.get_threads()
        return DownloaderConfig(url=url, path=path, chapter_strategy=chapter_strategy_config, threads=threads)

    def task_process_event_queue(self) -> None:
        self.event_manager.process_queue()
        self.container.after(100, self.task_process_event_queue)

    def set_events(self) -> None:
        OnQuit(self.event_manager).subscribe(self.on_quit)
        self.container.bind("<Escape>", lambda _: OnQuit(self.event_manager).emit())
        self.container.protocol("WM_DELETE_WINDOW", lambda: OnQuit(self.event_manager).emit())

    def on_quit(self) -> None:
        exit = messagebox.askyesno(title="Exit", message="Do you want to exit MangaDanga?")
        if exit:
            self.container.destroy()


class TopBanner:
    def __init__(self, container: Misc) -> None:
        self.label = ttk.Label(container, text="MangaDanga", anchor=tkinter.CENTER, style="TopBanner.TLabel")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.NSEW)


class NotebookComponent:
    def __init__(self, container: Misc, init_config: DownloaderConfig) -> None:
        self.notebook = ttk.Notebook(container, style="TNotebook")
        self.notebook.grid(row=1, column=0)
        self.download_tab = DownloadTab(self.notebook, init_config)
        self.settings_tab = SettingsTab(self.notebook, init_config)


class DownloadButton:
    def __init__(
        self,
        container: Misc,
        get_config: Callable[[], DownloaderConfig],
        event_manager: EventManager,
    ) -> None:
        self.container = container
        self.get_config = get_config
        self.event_manager = event_manager
        self.button = ttk.Button(
            self.container,
            text="Download",
            command=OnStartDownload(self.event_manager).emit,
            width=15,
            style="TButton",
        )
        self.button.grid(row=2, column=0, ipady=1, padx=10, pady=10)
        self.set_events()

    def set_events(self) -> None:
        OnStartDownload(self.event_manager).subscribe(self.on_start_download)
        OnDownloadFinished(self.event_manager).subscribe(self.on_download_finished)
        OnDownloadFinishedGUI(self.event_manager).subscribe(self.on_download_finished_gui)
        self.button.bind("<Return>", lambda _: OnStartDownload(self.event_manager).emit())

    def on_start_download(self) -> None:
        try:
            self.process_download()
        except DownloaderException as e:
            status = "warning"
            message = str(e)
            logger.exception(e)
        except Exception as e:
            status = "error"
            message = str(e)
            logger.exception(e)
        else:
            status = "ok"
            message = ""
        finally:
            OnDownloadFinishedGUI(self.event_manager).emit(status, message)

    def process_download(self) -> None:
        config = self.get_config()
        downloader = downloader_factory(config)
        self.button["state"] = "disabled"
        ProgressWindow(self.container, self.event_manager)
        self.threaded_coro(downloader.download())

    def on_download_finished(self, status: Literal["success", "warning", "error"], message: str) -> None:
        OnCloseProgress(self.event_manager).emit()
        OnDownloadFinishedGUI(self.event_manager).emit(status, message)

    def on_download_finished_gui(self, status: Literal["success", "warning", "error"], message: str) -> None:
        if status == "success":
            messagebox.showinfo(title="MangaDanga", message="Mandanga completed!")
        elif status == "warning":
            messagebox.showwarning(title="Warning!", message=message)
        elif status == "error":
            messagebox.showerror(title="Error!", message=f"Something unexpected happened: {message}")
        else:
            pass
        self.button["state"] = "normal"

    def threaded_coro(self, coro: Coroutine[Any, Any, None]) -> None:
        thread = threading.Thread(target=asyncio.run, args=(coro,))
        thread.start()


class ProgressWindow:
    def __init__(self, container: Misc, event_manager: EventManager) -> None:
        self.container = container
        self.event_manager = event_manager
        self.top_level_win = self.set_top_level_win()
        self.progress_bar = ttk.Progressbar(self.top_level_win, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()
        self.progress_label = ttk.Label(self.top_level_win, text="Receiving manga info...", style="Generic.TLabel")
        self.progress_label.pack()
        self.set_events()

    def set_top_level_win(self) -> tkinter.Toplevel:
        top_level_win = tkinter.Toplevel(self.container)
        top_level_win.title("Progress")
        top_level_win.iconbitmap(
            r"C:\Users\lpard\repos\manga-app\mangadanga\gui\static\Guts.ico"
        )  # This is for windows
        top_level_win.resizable(False, False)
        top_level_win.transient(self.container)
        top_level_win.configure(background="lavender")
        return top_level_win

    def set_events(self) -> None:
        OnChapterDownloadFinished(self.event_manager).subscribe(self.on_chapter_download_finished)
        OnMangaInfoUpdate(self.event_manager).subscribe(self.on_manga_info_updated)
        OnCloseProgress(self.event_manager).subscribe(self.on_close_progress)

    def update_label(self) -> None:
        self.progress_label[
            "text"
        ] = f"Chapters downloaded {self.progress_bar['value']}/{self.progress_bar['maximum']}"

    def on_manga_info_updated(self, chapter_count: int) -> None:
        logger.info(f"Received manga info. Chapter count: {chapter_count}")
        self.progress_bar["maximum"] = chapter_count
        self.progress_bar["value"] = 0
        self.update_label()

    def on_chapter_download_finished(self) -> None:
        self.progress_bar["value"] += 1
        self.update_label()

    def on_close_progress(self) -> None:
        OnChapterDownloadFinished(self.event_manager).unsubscribe(self.on_chapter_download_finished)
        OnMangaInfoUpdate(self.event_manager).unsubscribe(self.on_manga_info_updated)
        OnCloseProgress(self.event_manager).unsubscribe(self.on_close_progress)
        self.top_level_win.destroy()


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
            font=("consolas", 9),
            style="TEntry",
        )
        self.text.grid(row=0, column=0, columnspan=2, ipady=2, padx=10, pady=10, sticky=tkinter.EW)
        self.text.focus()

    def get_url(self) -> str:
        url = self.url_value.get()
        validate_non_empty(url, "URL")
        return url


class LocalPathComponent:
    def __init__(self, container: Misc, init_config: DownloaderConfig) -> None:
        self.init_config = init_config
        self.label_frame = ttk.Labelframe(container, text="Save to", style="TLabelframe")
        self.label_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NEW")
        self.path_value = tkinter.StringVar(value=self.init_config.path)
        self.text = ttk.Entry(
            self.label_frame, textvariable=self.path_value, width=36, font=("consolas", 9), style="TEntry"
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
        self.button.bind("<Return>", lambda _: self.handle_browse_button())

    def handle_browse_button(self) -> None:
        save_to_path = filedialog.askdirectory(initialdir=self.init_config.path)
        self.path_value.set(save_to_path)

    def get_path(self) -> str:
        path = self.path_value.get()
        validate_non_empty(path, "Save to")
        return path


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
        self.chapter_list_entry = self.set_chapters_entry()
        self.chapter_range_lower_bound_entry = self.set_chapter_range_entry_lower_bound()
        self.set_chapter_range_separator_label()
        self.chapter_range_upper_bound_entry = self.set_chapter_range_entry_upper_bound()
        self.radio_input.trace_add("write", lambda *_: self.on_radio_button_change())
        self.radio_input.set(0)

    def set_radiobuttons(self) -> None:
        chapter_options = ["All chapters", "Chapter/s", "Chapter range"]
        for index, text in enumerate(chapter_options):
            radiobutton = tkinter.Radiobutton(
                self.label_frame,
                text=text,
                variable=self.radio_input,
                value=index,
                font=("consolas", 10),
                background="lavender",
                activebackground="lavender",
                highlightthickness=0,
            )
            radiobutton.grid(row=index, column=0, padx=10, pady=10, sticky=tkinter.W)

    def set_chapters_entry(self) -> ttk.Entry:
        chapter_list_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_list_input,
            width=10,
            font=("consolas", 9),
            style="TEntry",
        )
        chapter_list_entry.grid(row=1, column=2, columnspan=3, ipady=2, padx=10, pady=10, sticky=tkinter.EW)
        return chapter_list_entry

    def set_chapter_range_entry_lower_bound(self) -> ttk.Entry:
        chapter_range_lower_bound_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_range_lower_bound_input,
            width=3,
            font=("consolas", 9),
            style="TEntry",
        )
        chapter_range_lower_bound_entry.grid(row=2, column=2, ipady=2, padx=10, pady=10, sticky=tkinter.EW)
        return chapter_range_lower_bound_entry

    def set_chapter_range_separator_label(self) -> None:
        self.separator_label = ttk.Label(self.label_frame, text="To", anchor=tkinter.CENTER, style="Generic.TLabel")
        self.separator_label.grid(row=2, column=3, padx=10, pady=10)

    def set_chapter_range_entry_upper_bound(self) -> ttk.Entry:
        chapter_range_upper_bound_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_range_upper_bound_input,
            width=3,
            font=("consolas", 9),
            style="TEntry",
        )
        chapter_range_upper_bound_entry.grid(row=2, column=4, ipady=2, padx=10, pady=10, sticky=tkinter.EW)
        return chapter_range_upper_bound_entry

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
        clean_chapters = []
        for chapter in chapters_list:
            validate_numeric(chapter, "Chapter/s")
            clean_chapters.append(chapter)
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
        validate_non_empty(raw_bound, "Chapter range bound")
        validate_numeric(raw_bound, "Chapter range bound")
        return raw_bound

    def on_radio_button_change(self) -> None:
        index = self.radio_input.get()
        if index == 0:
            self.chapter_list_entry["state"] = "disabled"
            self.chapter_range_lower_bound_entry["state"] = "disabled"
            self.chapter_range_upper_bound_entry["state"] = "disabled"
            self.chapter_list_input.set("")
            self.chapter_range_lower_bound_input.set("")
            self.chapter_range_upper_bound_input.set("")
        elif index == 1:
            self.chapter_list_entry.focus()
            self.chapter_list_entry["state"] = "normal"
            self.chapter_range_lower_bound_entry["state"] = "disabled"
            self.chapter_range_upper_bound_entry["state"] = "disabled"
            self.chapter_range_lower_bound_input.set("")
            self.chapter_range_upper_bound_input.set("")
        elif index == 2:
            self.chapter_range_lower_bound_entry.focus()
            self.chapter_list_entry["state"] = "disabled"
            self.chapter_range_lower_bound_entry["state"] = "normal"
            self.chapter_range_upper_bound_entry["state"] = "normal"
            self.chapter_list_input.set("")


class MultithreadingComponent:
    def __init__(self, container: Misc, init_config: DownloaderConfig) -> None:
        self.label_frame = ttk.Labelframe(container, text="Multithreading", style="TLabelframe")
        self.label_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky=tkinter.EW)
        self.label_frame.columnconfigure(0)
        self.label_frame.columnconfigure(1)
        self.label = ttk.Label(self.label_frame, text="Number of threads:", style="Generic.TLabel")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.W)
        self.combo_box = ttk.Combobox(
            self.label_frame, values=list(map(str, range(1, 11))), width=3, font=("consolas", 9)
        )
        self.combo_box.set(init_config.threads)
        self.combo_box.grid(row=0, column=1, ipady=2, padx=10, pady=10)

    def get_threads(self) -> int:
        raw_threads = self.combo_box.get()
        validate_non_empty(raw_threads, "Number of threads")
        validate_numeric(raw_threads, "Number of threads")
        return int(raw_threads)
