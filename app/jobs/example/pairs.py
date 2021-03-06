'''
There is a large pile of socks that must be paired by color. 
Given an array of integers representing the color of each sock, determine 
how many pairs of socks with matching colors there are.
'''
import json
from pulzarcore.core_jobs import CoreJobs


class Fibonacci(CoreJobs):
    def __init__(self, params):
        super.__init__(params)

    def sockMerchant(self, ar) -> int:
        '''Get pairs

        Parameters
        ----------
        ar : list
            Lis with pairs as integer
        
        Return
        ------
        int
            Numbers of pairs
        '''
        solution = 0
        frecuency = {}
        for item in ar:
            if item not in frecuency:
                frecuency.setdefault(item, 1)
            else:
                frecuency[item] += 1
        
        for _, val in frecuency.items():
            if val >= 2:
                tmp = val
                while tmp > 1:
                    if tmp % 2 == 0:
                        solution += 1
                    tmp -= 1

        return solution

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        array = json.loads(self.pulzar_parameters['array'])
        self.pulzar_set_output('Pairs found: {}'.format(
            self.sockMerchant(array)
        ))        

    def execute(self):
        '''
        Description: Example for ordering pairs
        Arguments: {"array": []}
        Category: Examples
        Author: Mauricio Cleveland
        '''
        self.run_my_code()
        return self.is_the_job_ok()
