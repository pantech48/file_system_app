"""
A module for configuring a logger with a specified name, level, log format, and filename.
"""
import logging
import os.path

from config.config_parser import config


class Logger:
    """
    A class for configuring a logger with a specified name, level, log format, and filename.

    Attributes:
        name (str): The name of the logger. Defaults to the name of the current module.
        level (int): The logging level. Defaults to logging.DEBUG.
        log_format (logging.Formatter): The log message format.
        filename (str): The name of the log file. Defaults to 'log.log'.
        logger (logging.Logger): The logger object created using the specified configuration.

    Methods:
        setup(): Configures the logger with the specified configuration and returns the logger object.
    """
    def __init__(self, name: str = __name__, level: int = logging.DEBUG,
                 log_format: str = config()["LOGGER"]["logger_formatter"],
                 filename: str = config()["LOGGER"]["logs_path"]) -> None:
        """
        Initializes the Logger object with the specified configuration.

        :param name: The name of the logger. Defaults to the name of the current module.
        :type name: str
        :param level: The logging level. Defaults to logging.DEBUG.
        :type level: int
        :param log_format: The log message format.
        :type log_format: str
        :param filename: The name of the log file. Defaults to 'log.log'.
        :type filename: str
            """
        self.name = name
        self.level = level
        self.log_format = logging.Formatter(log_format)
        self.filename_path = os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
        self.logger = logging.getLogger(self.name)

    def setup(self) -> logging.Logger:
        """
        Configures the logger with the specified configuration and returns the logger object.

        :return: The logger object configured with the specified configuration.
        :rtype: logging.Logger
        """
        if not self.logger.handlers:
            self.logger.setLevel(self.level)
            file_handler = logging.FileHandler(self.filename_path)
            file_handler.setLevel(self.level)
            file_handler.setFormatter(self.log_format)

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(self.log_format)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

        return self.logger


logger = Logger().setup()




