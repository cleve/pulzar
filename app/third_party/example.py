import json

class Example:
    def __init__(self, arg1):
        self.arg1 = arg1
    
    def hello(self):
        print('Hello example with arg ', self.arg1)
    
    def json_return(self):
        return json.dumps({'my_arg': self.arg1})

def execute(arguments):
    example = Example(arguments[0])
    example.hello()
    return example.json_return()