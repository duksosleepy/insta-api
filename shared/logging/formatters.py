class LogFormatter:
    """Standard log formatters for different outputs."""

    @property
    def console_format(self) -> str:
        """Colorized format for console output."""
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

    @property
    def file_format(self) -> str:
        """Standard format for file output."""
        return (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        )

    @property
    def access_format(self) -> str:
        """Format for API access logs."""
        return (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{extra[method]} {extra[url]} | "
            "{extra[status_code]} | "
            "{extra[duration]}ms | "
            "{message}"
        )

    @property
    def json_format(self) -> str:
        """JSON format for structured logging."""
        return (
            '{"timestamp": "{time:YYYY-MM-DDTHH:mm:ss.SSSZ}", '
            '"level": "{level}", '
            '"logger": "{name}", '
            '"function": "{function}", '
            '"line": "{line}", '  # Fixed: Added quotes around {line}
            '"message": "{message}"}'
        )
