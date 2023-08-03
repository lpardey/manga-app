# Standard Library
from argparse import ArgumentParser

PROGRAM_NAME = "MangaDanga"
PROGRAM_DESCRIPTION = (
    "Download your favorite graphic novels! "
    "A directory named after the novel will be created along with zip files for its chapter/s with its corresponding images."
    "By default, the downloaded files will be stored where you execute the program. Enjoy!"
)
PROGRAM_EPILOG = "Chachi"
PROGRAM_URL_HELP = "Display a url of the graphic novel to download"
PROGRAM_PATH_HELP = "Display the system path where the files will be stored"
PROGRAM_THREADS_HELP = "Display a number of threads to use"
PROGRAM_C_HELP = "Display the chapter/s required to download. It takes one or more numbers"
PROGRAM_R_HELP = (
    "Display the range of chapters required to download. It takes two numbers, the first smaller than the second"
)


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION,
        epilog=PROGRAM_EPILOG,
    )
    parser.add_argument("url", help=PROGRAM_URL_HELP)
    parser.add_argument("-p", "--path", nargs="?", default=".", help=PROGRAM_PATH_HELP)
    parser.add_argument("-t", "--threads", default=1, type=int, help=PROGRAM_THREADS_HELP)
    exclusive_group = parser.add_mutually_exclusive_group()
    exclusive_group.add_argument("-c", "--chapters", nargs="+", type=str, help=PROGRAM_C_HELP)
    exclusive_group.add_argument("-r", "--chapter_range", nargs=2, type=str, help=PROGRAM_R_HELP)
    return parser
