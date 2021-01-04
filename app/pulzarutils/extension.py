from abc import abstractmethod
from abc import ABCMeta
from os import remove

class Extension(metaclass=ABCMeta):
    '''Base class to implement extensions
    '''
    # Can be used in some cases
    file_path = None

    @abstractmethod
    def execute(self, params, file_path=None):
        '''Entrance for extensios
        '''
        return

    def clean_tmp(self):
        '''Clear temporal files, unused binary files
        after the process
        '''
        try:
            if self.file_path is not None:
                remove(self.file_path)
        except BaseException as err:
            print(err)


