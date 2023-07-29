import asyncio
import threading
import tkinter
from tkinter import Misc, ttk, filedialog, messagebox
from mangadanga.downloader import downloader_factory, DownloaderConfig
from typing import Callable, Literal
import logging
from mangadanga.events import EventManager, EVENT_MANAGER, OnCloseProgress
from ..downloader.config import ChapterStrategyConfig
from ..downloader.exceptions import DownloaderException
from .utils import validate_non_empty, validate_numeric

logger = logging.getLogger("MangaDanga-GUI")


class MainWindow:
    def __init__(
        self, container: tkinter.Tk, init_config: DownloaderConfig, event_manager: EventManager = EVENT_MANAGER
    ) -> None:
        self.init_config = init_config
        self.container = container
        self.top_banner = TopBanner(container)
        self.main_tabs = NotebookComponent(container, init_config)
        self.download_button = DownloadButton(container, self.get_config, event_manager=event_manager)
        self.event_manager = event_manager
        self.task_process_event_queue()
        self.window_general_management()

    def task_process_event_queue(self) -> None:
        self.event_manager.process_queue()
        self.container.after(100, self.task_process_event_queue)

    def get_config(self) -> DownloaderConfig:
        url = self.main_tabs.download_tab.url_component.get_url()
        path = self.main_tabs.download_tab.local_path_component.get_path()
        chapter_strategy_config = self.main_tabs.settings_tab.download_management.get_chapter_selection_strategy()
        threads = self.main_tabs.settings_tab.multithreading.get_threads()
        return DownloaderConfig(url=url, path=path, chapter_strategy=chapter_strategy_config, threads=threads)

    def window_general_management(self) -> None:
        self.container.bind("<Escape>", lambda _: self.quit())
        self.container.protocol("WM_DELETE_WINDOW", lambda: self.quit())

    def quit(self) -> None:
        exit = messagebox.askyesno(title="Exit", message="Do you want to exit MangaDanga?")
        if exit:
            self.container.destroy()


class ProgressWindow:
    def __init__(self, container: tkinter.Toplevel | None = None, event_manager: EventManager = EVENT_MANAGER) -> None:
        self.container = container or tkinter.Toplevel()
        self.container.title("Progress")
        self.container.resizable(False, False)
        self.progress_bar = ttk.Progressbar(self.container, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()
        self.progress_label = ttk.Label(self.container, text="Receiving manga info...")
        self.progress_label.pack()
        self.event_manager = event_manager
        self.event_manager.subscribe("chapter_download_finished", self.on_chapter_download_finished)
        self.event_manager.subscribe("manga_info_updated", self.on_manga_info_updated)
        # OnCloseProgress(self.event_manager).subscribe(self.on_close_progress)
        self.event_manager.subscribe("close_progress", self.on_close_progress)

    def setup_widgets(self) -> None:
        pass

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
        self.event_manager.unsubscribe("chapter_download_finished", self.on_chapter_download_finished)
        self.event_manager.unsubscribe("manga_info_updated", self.on_manga_info_updated)
        self.event_manager.unsubscribe("close_progress", self.on_close_progress)
        self.container.destroy()


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
    def __init__(
        self,
        container: Misc,
        get_config: Callable[[], DownloaderConfig],
        event_manager: EventManager = EVENT_MANAGER,
    ) -> None:
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
        self.button.bind("<Return>", lambda _: self.handle_download_button())
        self.event_manager = event_manager
        self.event_manager.subscribe("download_finished", self.on_download_finished)
        self.event_manager.subscribe("init_download", self.on_init_download)
        self.event_manager.subscribe("download_finished_gui", self.on_download_finished_gui)
        self.event_manager.subscribe("start_download", self.on_start_download)

    def on_init_download(self) -> None:
        self.button["state"] = "disabled"
        ProgressWindow()

    def on_download_finished(self, status: Literal["success", "error"], message: str) -> None:
        self.event_manager.emit("close_progress")
        self.event_manager.emit("download_finished_gui", status, message)

    def on_download_finished_gui(self, status: Literal["success", "error"], message) -> None:
        if status == "success":
            messagebox.showinfo(title="MangaDanga", message="Mandanga completed!")
        else:
            messagebox.showerror(title="Error!", message=f"Something unexpected happened: {message}")
        self.button["state"] = "normal"

    def threaded_coro(self, coro) -> None:
        thread = threading.Thread(target=asyncio.run, args=(coro,))
        thread.start()

    def handle_download_button(self) -> None:
        try:
            config = self.get_config()
            self.event_manager.emit("init_download")
            self.event_manager.emit("start_download", config)
        except DownloaderException as e:
            logger.exception(e)
            messagebox.showwarning(title="Warning!", message=e)
        except Exception as e:
            logger.exception(e)
            messagebox.showerror(title="Error!", message=f"Something unexpected happened: {e}")

    def on_start_download(self, config: DownloaderConfig) -> None:
        downloader = downloader_factory(config)
        self.threaded_coro(downloader.download())


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

        self.url_value = tkinter.StringVar(value="https://chapmanganato.com/manga-pf958088")
        self.text = ttk.Entry(
            self.label_frame,
            textvariable=self.url_value,
            width=50,
            font=("consolas", 8),
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
        self.button.bind("<Return>", lambda _: self.handle_browse_button())

    def get_path(self) -> str:
        path = self.path_value.get()
        validate_non_empty(path, "Save to")
        return path

    def handle_browse_button(self) -> None:
        try:
            save_to_path = filedialog.askdirectory(initialdir=self.init_config.path)
            if save_to_path != "":
                self.path_value.set(save_to_path)
        except Exception as e:
            logger.exception(e)
            messagebox.showerror(title="Error!", message=f"Something unexpected happened: {e}")


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
        self.chapter_list_entry: ttk.Entry
        self.chapter_range_lower_bound_entry: ttk.Entry
        self.chapter_range_upper_bound_entry: ttk.Entry
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
        self.radio_input.trace_add("write", lambda *_: self.on_radio_button_change())
        self.radio_input.set(0)

    def disable_chapter_list_entry(self) -> None:
        self.chapter_list_entry["state"] = "disabled"

    def enable_chapter_list_entry(self) -> None:
        self.chapter_list_entry["state"] = "normal"

    def disable_chapter_range_entries(self) -> None:
        self.chapter_range_lower_bound_entry["state"] = "disabled"
        self.chapter_range_upper_bound_entry["state"] = "disabled"

    def enable_chapter_range_entries(self) -> None:
        self.chapter_range_lower_bound_entry["state"] = "normal"
        self.chapter_range_upper_bound_entry["state"] = "normal"

    def on_radio_button_change(self) -> None:
        index = self.radio_input.get()
        if index == 0:
            self.disable_chapter_list_entry()
            self.disable_chapter_range_entries()
        elif index == 1:
            self.enable_chapter_list_entry()
            self.disable_chapter_range_entries()
        elif index == 2:
            self.disable_chapter_list_entry()
            self.enable_chapter_range_entries()

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
        self.chapter_list_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_list_input,
            width=10,
            font=("consolas", 8),
            style="TEntry",
        )
        self.chapter_list_entry.grid(row=1, column=2, columnspan=3, ipady=2, padx=10, pady=10, sticky=tkinter.EW)

    def set_chapter_range_entry_lower_bound(self) -> None:
        self.chapter_range_lower_bound_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_range_lower_bound_input,
            width=3,
            font=("consolas", 8),
            style="TEntry",
        )
        self.chapter_range_lower_bound_entry.grid(row=2, column=2, ipady=2, padx=10, pady=10, sticky=tkinter.EW)

    def set_chapter_range_separator_label(self) -> None:
        self.separator_label = ttk.Label(self.label_frame, text="To", anchor=tkinter.CENTER, style="Generic.TLabel")
        self.separator_label.grid(row=2, column=3, padx=10, pady=10)

    def set_chapter_range_entry_upper_bound(self) -> None:
        self.chapter_range_upper_bound_entry = ttk.Entry(
            self.label_frame,
            textvariable=self.chapter_range_upper_bound_input,
            width=3,
            font=("consolas", 8),
            style="TEntry",
        )
        self.chapter_range_upper_bound_entry.grid(row=2, column=4, ipady=2, padx=10, pady=10, sticky=tkinter.EW)

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
        validate_non_empty(raw_bound, "Chapter range bound")
        validate_numeric(raw_bound, "Chapter range bound")
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

    def get_threads(self) -> int:
        raw_threads = self.combo_box.get()
        validate_non_empty(raw_threads, "Threads")
        validate_numeric(raw_threads, "Threads")
        return int(raw_threads)
