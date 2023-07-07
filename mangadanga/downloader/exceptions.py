class DownloaderException(Exception):
    pass


class DownloaderExceptionUrlWithoutCoverage(DownloaderException):
    def __init__(self, message: str = "URL not registered in MangaDanga!") -> None:
        self.message = message
        super().__init__(self.message)


class DownloaderExceptionInvalidPattern(DownloaderException):
    def __init__(
        self,
        message: str = "Invalid argument pattern. A valid pattern consists of two numbers where first one is smaller than the second ,e.g., '1-8'",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class DownloaderExceptionUnexpected(DownloaderException):
    pass
