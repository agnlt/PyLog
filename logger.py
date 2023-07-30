"""
PyLog is a very simple logger written in Python.

Copyright © Antonin GENELOT, 30/07/2023
"""

from enum import Enum
from datetime import datetime
import os
import re


class LogLevel(Enum):
    Info = 0,
    Warning = 1,
    Error = 2

class Logger:
    def __init__(self, log_level: LogLevel = LogLevel.Info, log_to_file: bool = False) -> None:
        self.log_level = log_level

        self._log_to_file = log_to_file
        self._date = datetime.now()
        self._filename = 'logs.txt'
        self.RESET  = '\033[0m'
        self.RED    = '\033[0;31m'
        self.BLUE   = '\033[0;36m'
        self.YELLOW = '\033[0;33m'
        self.BOLD   = '\033[1m'


    #######################
    # Private methods
    ######################

    def __log_level_to_string(self, log_level: LogLevel=None) -> str:
        """
        Returns the stringified version of the log level parameter if it is not None,
        else returns the stringified versoin of the current log level.
        """
        if log_level is None: level = self.log_level
        else: level = log_level
        match level:
            case LogLevel.Info:
                return 'info'
            case LogLevel.Warning:
                return 'warning'
            case LogLevel.Error:
                return 'error'
        return 'info'


    def __format_date(self) -> str:
        """
        Returns the date using `dd/mm/yyyy` format.
        """
        day = str(self._date.day)
        month = str(self._date.month)
        if int(day) < 10:
            day = '0' + day
        if int(month) < 10:
            month = '0' + month
        return f'{day}/{month}/{self._date.year}'


    def __strip_format(self, input_string: str) -> str:
        """
        Removes all the ANSI escape codes from the given string.
        """
        escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return escape.sub('', input_string)


    def __get_format(self, color: str, log_level: LogLevel) -> str:
        """
        Default string format for the logger, aka `(bold + color)[date] severity:(no bold + color)`.
        """
        return f'{color}{self.BOLD}[{self.__format_date()}] {self.__log_level_to_string(log_level).upper()}:{self.RESET}{color}'


    def __write_to_file(self, format: str) -> None:
        """
        Writes the `format` to a file called `logs.txt` and removes the ANSI escapes code from the format.
        """
        with open(self._filename, 'a+') as logs:
            logs.write(self.__strip_format(format) + '\n')


    ##########################
    # Public methods
    #########################

    def reset(self) -> None:
        """
        Resets the log level to LogLevel.Info.
        """
        self.log_level = LogLevel.Info


    def log(self, format: str):
        """
        Logs a message with the current log level.
        """
        match self.log_level:
            case LogLevel.Info:
                self.info(format)
            case LogLevel.Warning:
                self.warning(format)
            case LogLevel.Error:
                self.error(format)
            case other:
                pass


    def info(self, format: str) -> None:
        """
        Logs the message in blue using `self.__get_format()`.
        """
        if self._log_to_file:
            self.__write_to_file(format)
        print(f'{self.__get_format(self.BLUE, LogLevel.Info)} {format}')
        print(self.RESET)


    def warning(self, format: str) -> None:
        """
        Logs the message in yellow using `self.__get_format()`.
        """
        if self._log_to_file:
            self.__write_to_file(format)
        print(f'{self.__get_format(self.YELLOW, LogLevel.Warning)} {format}')
        print(self.RESET)


    def error(self, format: str) -> None:
        """
        Logs the message in red using `self.__get_format()`.
        """
        if self._log_to_file:
            self.__write_to_file(format)
        print(f'{self.__get_format(self.RED, LogLevel.Error)} {format}')
        print(self.RESET)


    def set_level(self, log_level: LogLevel) -> None | ValueError:
        """
        Sets the current log level. An ValueError is raised if the log level provided is incorrect.
        """
        if log_level not in [LogLevel.Info, LogLevel.Warning, LogLevel.Error]:
            raise ValueError('log_level must be LogLevel.{Info, Warning, Error}')
        self.log_level = log_level


    def enable_file_logging(self) -> None:
        """
        Enables logging to a file.
        """
        self._log_to_file = True


    def disable_file_logging(self) -> None:
        """
        Disables logging to a file.
        """
        self._log_to_file = False


    def clean_logs(self) -> None:
        """
        Removes the file `logs.txt` if it existed.
        """
        if os.path.exists(self._filename):
            os.remove(self._filename)
