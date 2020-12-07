from pulzarutils.extension import Extension


class Example(Extension):
    def __init__(self, arguments, params, file_path=None):
        '''Receiving values
            URL: http://master:[port]/extension/arg_1/arg_2/arg_n?param_1=1&param_2=2&param_n=n

        arguments
        ---------
        arguments = ['arg_1', 'arg_2', 'arg_n']

        parameters
        ----------
        params = {'param_1': [1], 'param_2': [2], 'param_n': [n]}
        '''

        self.args = arguments
        self.params = params

    def hello(self):
        if len(self.args) > 0:
            print('Hello example with arg ', self.args)

    def method_return(self):
        return {'my_arg': self.args, 'my_params': self.params}

    def execute(self):
        '''Mandatory name
        '''
        self.hello()
        return self.method_return()
