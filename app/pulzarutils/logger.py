import logging

class PulzarLogger:
    def __init__(self, const):
        self.const = const
        self.logger = logging.getLogger(self.__class__.__name__)
        self.format = '%(asctime)s:%(levelname)s:%(message)s'

    def set_up(self, level, file_path) -> None:
        '''Set logging level
        
        Parameters
        ----------
        level : str
            Values allowed:
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
        self.file_handler = logging.handlers.RotatingFileHandler(
            file_path, maxBytes=100000, backupCount=5)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        if level == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif level == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            self.logger.setLevel(logging.ERROR)

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

    def exeption(self, message) -> None:
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