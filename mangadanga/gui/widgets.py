from tkinter import *
from tkinter import ttk


class GUIWidgets:
    def __init__(self, master: Tk) -> None:
        self.master = master

    def set_widgets(self) -> None:
        self.set_main_title()
        self.set_notebook()
        self.set_download_button()

    def set_main_title(self) -> None:
        title_label = ttk.Label(self.master, text="MangaDanga", anchor=CENTER, style="Title.TLabel")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def set_notebook(self) -> None:
        notebook = ttk.Notebook(self.master, style="TNotebook")
        notebook.grid(row=1, column=0)
        self.set_notebook_content(notebook)

    def set_notebook_content(self, notebook: ttk.Notebook) -> None:
        download_frame = self.set_notebook_download_frame(notebook)
        settings_frame = self.set_notebook_settings_frame(notebook)
        self.notebook_frames_config(download_frame, settings_frame)
        self.set_dowload_frame_content(download_frame)
        self.set_settings_frame_content(settings_frame)

    def set_notebook_download_frame(self, notebook: ttk.Notebook) -> ttk.Frame:
        download_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(download_frame, text="Download")
        return download_frame

    def set_notebook_settings_frame(self, notebook: ttk.Notebook) -> ttk.Frame:
        settings_frame = ttk.Frame(notebook, style="TFrame")
        notebook.add(settings_frame, text="Settings")
        return settings_frame

    def notebook_frames_config(self, download_frame: ttk.Frame, settings_frame: ttk.Frame) -> None:
        download_frame.columnconfigure(0, weight=1)
        download_frame.columnconfigure(1, weight=1)
        download_frame.rowconfigure(0, weight=1)
        download_frame.rowconfigure(1, weight=1)
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)

    def set_dowload_frame_content(self, download_frame: ttk.Frame) -> None:
        self.set_url_label_frame(download_frame)
        self.set_save_to_label_frame(download_frame)

    def set_url_label_frame(self, download_frame: ttk.Frame) -> None:
        url_lf = ttk.Labelframe(download_frame, text="URL", style="TLabelframe")
        url_lf.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=EW)
        self.set_url_entry(url_lf)

    def set_url_entry(self, url_lf: ttk.Labelframe) -> None:
        url_input = StringVar()
        url_entry = ttk.Entry(url_lf, textvariable=url_input, width=50, font=("consolas", 8), style="TEntry")
        url_entry.grid(row=0, column=0, columnspan=2, ipady=2, padx=10, pady=10, sticky=EW)

    def set_save_to_label_frame(self, download_frame: ttk.Frame) -> None:
        save_to_lf = ttk.Labelframe(download_frame, text="Save to", style="TLabelframe")
        save_to_lf.grid(row=1, column=0, padx=10, pady=10, sticky="NEW")
        self.set_save_to_entry(save_to_lf)
        self.set_browse_button(save_to_lf)

    def set_save_to_entry(self, save_to_lf: ttk.Labelframe) -> None:
        save_to_input = StringVar()
        save_to_entry = ttk.Entry(
            save_to_lf, textvariable=save_to_input, width=36, font=("consolas", 8), style="TEntry"
        )
        save_to_entry.grid(row=1, column=0, ipady=2, padx=10, pady=10, sticky="NEW")

    def set_browse_button(self, save_to_lf: ttk.Labelframe) -> None:
        browse_button = ttk.Button(save_to_lf, text="Browse", command=None, width=9, style="TButton")
        browse_button.grid(row=1, column=1, ipady=1, padx=10, pady=10)

    def set_download_button(self) -> None:
        start_button = ttk.Button(self.master, text="Download", command=None, width=15, style="TButton")
        start_button.grid(row=2, column=0, ipady=1, padx=10, pady=10)

    def set_settings_frame_content(self, settings_frame: ttk.Frame) -> None:
        self.set_download_management_lf(settings_frame)
        self.set_multithreading_lf(settings_frame)

    def set_download_management_lf(self, settings_frame: ttk.Frame) -> None:
        download_management_lf = ttk.Labelframe(settings_frame, text="Download Management", style="TLabelframe")
        download_management_lf.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky=EW)
        self.set_download_management_radiobuttons(download_management_lf)
        self.set_chapters_entry(download_management_lf)
        self.set_chapter_range_entry_1(download_management_lf)
        self.set_chapter_range_separator_label(download_management_lf)
        self.set_chapter_range_entry_2(download_management_lf)

    def set_download_management_radiobuttons(self, download_management_lf: ttk.Labelframe) -> None:
        global option  # The variable named Source is local to the function, i.e. is garbage collected when the function exits because you don't return it, hence is None and not a string or bytes like object.
        option = IntVar()
        option.set(1)
        radiobuttons = {"All chapters": 1, "Chapter/s:": 2, "Chapter range:": 3}
        row = 0
        for text, value in radiobuttons.items():
            radiobutton = Radiobutton(
                download_management_lf,
                text=text,
                variable=option,
                value=value,
                font=("consolas", 8),
                background="lavender",
                activebackground="lavender",
                highlightthickness=0,
            )
            radiobutton.grid(row=row, column=0, padx=10, pady=10, sticky=W)
            row += 1

    def set_chapters_entry(self, download_management_lf: ttk.Labelframe) -> None:
        chapter_input = StringVar()
        chapter_entry = ttk.Entry(
            download_management_lf,
            textvariable=chapter_input,
            width=10,
            font=("consolas", 8),
            style="TEntry",
        )
        chapter_entry.grid(row=1, column=2, columnspan=3, ipady=2, padx=10, pady=10, sticky=EW)

    def set_chapter_range_entry_1(self, download_management_lf: ttk.Labelframe) -> None:
        chapter_r1_input = StringVar()
        chapter_r1_entry = ttk.Entry(
            download_management_lf,
            textvariable=chapter_r1_input,
            width=3,
            font=("consolas", 8),
            style="TEntry",
        )
        chapter_r1_entry.grid(row=2, column=2, ipady=2, padx=10, pady=10, sticky=EW)

    def set_chapter_range_separator_label(self, download_management_lf: ttk.Labelframe) -> None:
        separator_label = ttk.Label(download_management_lf, text="To", anchor=CENTER, style="Generic.TLabel")
        separator_label.grid(row=2, column=3, padx=10, pady=10)

    def set_chapter_range_entry_2(self, download_management_lf: ttk.Labelframe) -> None:
        chapter_r2_input = StringVar()
        chapter_r2_entry = ttk.Entry(
            download_management_lf,
            textvariable=chapter_r2_input,
            width=3,
            font=("consolas", 8),
            style="TEntry",
        )
        chapter_r2_entry.grid(row=2, column=4, ipady=2, padx=10, pady=10, sticky=EW)

    def set_multithreading_lf(self, settings_frame: ttk.Frame) -> None:
        multithreading_lf = ttk.Labelframe(settings_frame, text="Multithreading", style="TLabelframe")
        multithreading_lf.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky=EW)
        multithreading_lf.columnconfigure(0)
        multithreading_lf.columnconfigure(1)
        self.set_multithreading_label(multithreading_lf)
        self.set_multithreading_combobox(multithreading_lf)

    def set_multithreading_label(self, multithreading_lf: ttk.Labelframe) -> None:
        multithreading_label = ttk.Label(multithreading_lf, text="Number of threads:", style="Generic.TLabel")
        multithreading_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

    def set_multithreading_combobox(self, multithreading_lf: ttk.Labelframe) -> None:
        multithreading_cb = ttk.Combobox(
            multithreading_lf,
            values=[value for value in range(1, 11)],
            width=3,
            font=("consolas", 8),
        )
        multithreading_cb.set(1)
        multithreading_cb.grid(row=0, column=1, ipady=2, padx=10, pady=10)
