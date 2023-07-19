from .gui.mangadanga_gui import MangadangaGUI
import logging


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app = MangadangaGUI()
    app.container.mainloop()


if __name__ == "__main__":
    main()
