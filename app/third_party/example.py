
class Example:
    def __init__(self, arg1):
        self.arg1 = arg1
    
    def hello(self):
        print('Hello example with arg ', self.arg1)

def execute(arguments):
    example = Example(arguments[0])
    example.hello()