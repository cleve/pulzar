from pulzarutils.extension import Extension


class Example(Extension):
    def __init__(self, arg1):
        self.arg1 = arg1

    def hello(self):
        print('Hello example with arg ', self.arg1)

    def method_return(self):
        return {'my_arg': self.arg1}


def execute(arguments, params):
    example = Example(arguments[0])
    example.hello()
    return example.method_return()
