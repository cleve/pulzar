from abc import abstractmethod
from abc import ABCMeta
from os import remove

class Extension(metaclass=ABCMeta):
    '''Base class to implement extensions
    '''
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.file_path = None
    
    @abstractmethod
    def execute(self):
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
            raise Exception('clean_tmp: error cleaning the space::' + str(err))


