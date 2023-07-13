from .gui.mangadanga_gui import MangadangaGUI


def main() -> None:
    app = MangadangaGUI()
    app.container.mainloop()


if __name__ == "__main__":
    main()
