import tempfile
import random
from pulzarcore.core_jobs import CoreJobs


class Factorial(CoreJobs):
    '''Example of job programation

    Factorial number
    ----------------

    f(0) = 0
    f(1) = 1
    f(n) = n * (n-1) * (n-2) * (n - 3) *... (1)

    eg: f(4) = 4 * 3 * 2 * 1
    '''

    def __init__(self, params):
        super().__init__(params)

    def factorial_recursion(self, number):
        '''Recursion method
        '''
        if number == 0:
            return 1
        return number * self.factorial_recursion(number - 1)

    def factorial_while(self, number):
        '''While method
        '''
        factorial = 1
        while number > 0:
            factorial = factorial * number
            number -= 1
        return factorial

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        number = int(self.pulzar_parameters['number'])
        self.pulzar_set_output('Factorial recursive: {}\nFactorial while: {}'.format(
            self.factorial_recursion(number),
            self.factorial_while(number)
        ))


def execute(arguments):
    """
    Description: Factorial number using recursion and while
    Arguments: {"number": "str"}
    Category: Examples
    Author: Mauricio Cleveland
    """
    example = Factorial(arguments)
    example.run_my_code()
    return example.is_the_job_ok()
