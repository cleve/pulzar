import time
from pulzarcore.core_jobs import CoreJobs


class Fibonacci(CoreJobs):
    '''Example of job programation

    Fibonacci number
    ----------------

    f(0) = 0
    f(1) = 1
    f(n) = f(n-1) + f(n-2)

    eg: f(4) = [0, 1, 1, 2, 3]
    '''

    def __init__(self, params):
        super().__init__(params)

    def fib_recursion(self, n):
        '''recursion solution
        '''
        if n == 0:
            return [0]
        if n == 1:
            return [0, 1]
        else:
            temp_sum = self.fib_recursion(n - 1)
        return temp_sum + [temp_sum[len(temp_sum) - 1] + temp_sum[len(temp_sum) - 2]]

    def fib_while(self, n):
        '''Using while
        '''
        serie = []
        init = 0
        while init <= n:
            if init in (0, 1):
                serie.append(init)
            else:
                serie.append(serie[len(serie) - 1] + serie[len(serie) - 2])
            init += 1
        return serie

    def fib_for(self, n):
        '''Using for
        '''
        serie = []
        for ii in range(n + 1):
            if ii == 0 or ii == 1:
                serie.append(ii)
            else:
                serie.append(serie[ii - 1] + serie[ii - 2])
        return serie

    def process_data(self):
        if self.pulzar_get_filepath() is not None:
            print('Opening ', self.pulzar_get_filepath())
            line_number = 1
            with open(self.pulzar_get_filepath(), 'rb') as f:
                for line in f:
                    print('(' + str(line_number) + ')', line.decode())
                    line_number += 1

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        number = int(self.pulzar_parameters['number'])
        self.pulzar_set_output('Recursion: {}\nWhile:{}\nFor:{}'.format(
            self.fib_recursion(number),
            self.fib_while(number),
            self.fib_for(number)
        ))

    def execute(self):
        '''
        Description: Fibonacci number using recursion and while
        Arguments: {"number": "int"}
        Category: Examples
        Author: Mauricio Cleveland
        '''
        self.run_my_code()
        return self.is_the_job_ok()

if __name__ == "__main__":
    ws = Fibonacci({'job_id': '-1', '_pulzar_config': 1, 'number': '4'})
    ws.local_exec = True
    ws.execute()
    # Print logs
    print(ws._log)

    # Print output
    print(ws._pulzar_job_output)