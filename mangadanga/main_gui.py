# Standard Library
import logging

# Local imports
from .gui.mangadanga_gui import MangadangaGUI


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    app = MangadangaGUI()
    app.container.mainloop()


if __name__ == "__main__":
    main()
