from abc import abstractmethod


class Extension:
    '''Base class to implement extensions
    '''

    @abstractmethod
    def execute(self, params, file_path=None):
        '''Entrance for extensios
        '''
        return
