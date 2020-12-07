from pulzarutils.extension import Extension


class Example(Extension):
    def __init__(self, arguments, params, file_path=None):
        self.args = arguments
        self.params = params

    def hello(self):
        if len(self.args) > 0:
            print('Hello example with arg ', self.args)

    def method_return(self):
        return {'my_arg': self.args, 'my_params': self.params}

    def execute(self):
        self.hello()
        return self.method_return()
