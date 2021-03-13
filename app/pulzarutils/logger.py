from pulzarutils.utils import Constants
import os
import logging
from logging.handlers import RotatingFileHandler

class PulzarLogger:
    def __init__(self, master=True):
        '''Logger class

        Should be instantiate once
        '''
        self.debug_console = Constants.DEBUG
        self.file_name = 'pulzar.log'
        if Constants.DEBUG and master:
            self.file_name = 'pulzarmaster.log'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.format = '%(asctime)s:%(levelname)s:%(message)s'
        self.set_up(Constants.DEBUG_LEVEL, Constants.LOG_PATH)

    def set_up(self, level, file_path) -> None:
        '''Set logging level
        
        Parameters
        ----------
        level : str
            Values allowed:
                - INFO
                - DEBUG
                - WARNING
                - ERROR
        file_path : str
            The path where the log will be stored
        Return
        ------
        None
        '''
        self.formatter = logging.Formatter(self.format)
        self.file_handler = RotatingFileHandler(
            os.path.join(file_path, self.file_name),
            maxBytes=1000000,
            backupCount=2
        )
        self.file_handler.setFormatter(self.formatter)
        if not self.logger.handlers:
            self.logger.addHandler(self.file_handler)
        if level == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            self.logger.setLevel(logging.ERROR)

    def info(self, message) -> None:
        '''Register info logs

        Parameters
        ----------
        message : str
            The message to be logged
        
        Return
        ------
        None
        '''
        self.logger.info(message)

    def debug(self, message) -> None:
        '''Register debug logs

        Parameters
        ----------
        message : str
            The message to be logged
        
        Return
        ------
        None
        '''
        self.logger.debug(message)

    def warning(self, message) -> None:
        '''Register warning logs

        Parameters
        ----------
        message : str
            The message to be logged
        
        Return
        ------
        None
        '''
        self.logger.warning(message)

    def error(self, message) -> None:
        '''Register error logs

        Parameters
        ----------
        message : str
            The message to be logged
        
        Return
        ------
        None
        '''
        self.logger.error(message)

    def exception(self, message) -> None:
        '''Register error with traceback logs

        Parameters
        ----------
        message : str
            The message to be logged
        
        Return
        ------
        None
        '''
        self.logger.exception(message)