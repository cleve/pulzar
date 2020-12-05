from abc import abstractmethod
from abc import ABCMeta


class Extension(metaclass=ABCMeta):
    '''Base class to implement extensions
    '''

    @abstractmethod
    def execute(self, params, file_path=None):
        '''Entrance for extensios
        '''
        return
