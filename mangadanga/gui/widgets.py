import asyncio
import tkinter
from tkinter import Misc, ttk, filedialog, messagebox
from mangadanga.downloader import downloader_factory, chapters_selection_factory, DownloaderConfig
from typing import Any, Callable


# class EventEmitter:
#     def __init__(self) -> None:
#         self.listeners: dict[str, list[Callable[..., Any]]] = {}

#     def add_listener(self, event: str, listener: Callable[..., Any]) -> None:
#         if event not in self.listeners:
#             self.listeners[event] = []
#         self.listeners[event].append(listener)

#     def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
#         if event not in self.listeners:
#             return
#         for listener in self.listeners[event]:
#             listener(*args, **kwargs)


# EVENT_EMITTER = EventEmitter()


# def mi_cosa(config: Config) -> None:
#     print(config)


# EVENT_EMITTER.add_listener(
#     "download_button_clicked", lambda config: asyncio.run(downloader_factory(config).download())
# )

# EVENT_EMITTER.emit("progress_update", id, progress)
import logging

logger = logging.getLogger("MangaDanga-GUI")


class MainWindow:
    def __init__(self, container: Misc, config: DownloaderConfig) -> None:
        self.config = config
        self.top_banner = TopBanner(container)
        self.main_tabs = NotebookComponent(container, config, self.handle_browse_button)
        self.download_button = DownloadButton(container, self.handle_download_button)

    def handle_download_button(self) -> None:
        config = self.get_config()
        downloader = downloader_factory(config)
        # EVENT_EMITTER.emit("download_button_clicked", config)
        try:
            asyncio.run(downloader.download())
            messagebox.showinfo(title="MangaDanga", message="Mandanga completed!")
        except Exception as e:
            logger.exception(e)
            messagebox.showerror(
                title="Error!",
                message=f"Something unexpected happened: {e}",
            )

    def handle_browse_button(self) -> None:
        save_to_path = filedialog.askdirectory(initialdir=self.config.path)
        self.field_missing(field=save_to_path, name="'Save to'")
        self.main_tabs.download_tab.local_path_component.path_value.set(save_to_path)

    def get_config(self) -> DownloaderConfig:
        url = self.field_missing(self.main_tabs.download_tab.url_component.url_value.get(), "'URL'")
        path = self.field_missing(self.main_tabs.download_tab.local_path_component.path_value.get(), "'Path'")
        chapter, chapter_range = self.get_chapter_and_chapter_range(
            self.main_tabs.settings_tab.download_management.radio_input.get(),
            self.main_tabs.settings_tab.download_management.chapter_list_input.get(),
            self.main_tabs.settings_tab.download_management.chapter_range_lower_bound_input.get(),
            self.main_tabs.settings_tab.download_management.chapter_range_upper_bound_input.get(),
        )
        chapter_strategy = chapters_selection_factory(chapter, chapter_range)
        threads = int(self.field_missing(self.main_tabs.settings_tab.multithreading.combo_box.get(), "'Threads'"))
        self.config.update_config_attrs(url, path, chapter_strategy, threads)
        return self.config

        # start_button.state(["disabled"]) if not url else start_button.state(["active"])

    def field_missing(self, field: str, name: str) -> str:
        if not field:
            raise Exception(messagebox.showwarning(title="Warning!", message=f"{name} field is missing."))
        else:
            return field

    def get_chapter_and_chapter_range(
        self,
        radiobutton_selection: int,
        chapter_input: str,
        chapter_range_lower_bound: str,
        chapter_range_upper_bound: str,
    ) -> tuple[None, None] | tuple[list[str], None] | tuple[None, tuple[str, str]]:
        chapter = None
        chapter_range = None
        if radiobutton_selection == 0:
            if any([chapter_input, chapter_range_lower_bound, chapter_range_upper_bound]):
                raise Exception(
                    messagebox.showerror(
                        title="Error!", message=f"'Chapter/s' and 'Chapter range' fields must be empty for this option"
                    )
                )
        elif radiobutton_selection == 1:
            if any([chapter_range_lower_bound, chapter_range_upper_bound]):
                raise Exception(
                    messagebox.showerror(
                        title="Error!", message=f"'Chapter range' fields must be empty for this option"
                    )
                )
            chapter = self.field_missing(chapter_input, "'Chapter/s'").split(" ")
        elif radiobutton_selection == 2:
            chapter_range = tuple(
                [
                    self.field_missing(chapter_range_lower_bound, "'Chapter range lower bound'"),
                    self.field_missing(chapter_range_upper_bound, "'Chapter range upper bound'"),
                ]
            )
        return chapter, chapter_range


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
    def __init__(self, container: Misc, config: DownloaderConfig, handle_click: Callable) -> None:
        self.notebook = ttk.Notebook(container, style="TNotebook")
        self.notebook.grid(row=1, column=0)
        self.download_tab = DownloadTab(self.notebook, config, handle_click)
        self.settings_tab = SettingsTab(self.notebook, config)


class DownloadButton:
    def __init__(self, container: Misc, handle_click: Callable) -> None:
        self.button = ttk.Button(container, text="Download", command=handle_click, width=15, style="TButton")
        self.button.grid(row=2, column=0, ipady=1, padx=10, pady=10)


class DownloadTab:
    def __init__(self, container: ttk.Notebook, config: DownloaderConfig, handle_click: Callable) -> None:
        self.frame = ttk.Frame(container, style="TFrame")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        container.add(self.frame, text="Download")

        self.url_component = UrlComponent(self.frame)
        self.local_path_component = LocalPathComponent(self.frame, config, handle_click)


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
    def __init__(self, container: Misc, config: DownloaderConfig, handle_click: Callable) -> None:
        self.label_frame = ttk.Labelframe(container, text="Save to", style="TLabelframe")
        self.label_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NEW")
        self.path_value = tkinter.StringVar(value=config.path)
        self.text = ttk.Entry(
            self.label_frame, textvariable=self.path_value, width=36, font=("consolas", 8), style="TEntry"
        )
        self.text.grid(row=1, column=0, ipady=2, padx=10, pady=10, sticky="NEW")

        self.button = ttk.Button(self.label_frame, text="Browse", command=handle_click, width=9, style="TButton")
        self.button.grid(row=1, column=1, ipady=1, padx=10, pady=10)


class SettingsTab:
    def __init__(self, container: ttk.Notebook, config: DownloaderConfig) -> None:
        self.frame = ttk.Frame(container, style="TFrame")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        container.add(self.frame, text="Settings")

        self.download_management = DownloadManagementComponent(self.frame)
        self.multithreading = MultithreadingComponent(self.frame, config)


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

        # radiobutton.bind(
        #     "<Button-1>", lambda event: self.event_emitter.emit(f"radio_button_{index}_clicked", event)
        # )

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


class MultithreadingComponent:
    def __init__(self, container: Misc, config: DownloaderConfig) -> None:
        self.label_frame = ttk.Labelframe(container, text="Multithreading", style="TLabelframe")
        self.label_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky=tkinter.EW)

        self.label_frame.columnconfigure(0)
        self.label_frame.columnconfigure(1)

        self.label = ttk.Label(self.label_frame, text="Number of threads:", style="Generic.TLabel")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky=tkinter.W)

        self.combo_box = ttk.Combobox(self.label_frame, values=list(range(1, 11)), width=3, font=("consolas", 8))
        self.combo_box.set(config.threads)
        self.combo_box.grid(row=0, column=1, ipady=2, padx=10, pady=10)
