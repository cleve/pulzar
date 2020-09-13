import time
from pulzarcore.core_jobs import CoreJobs


class Example(CoreJobs):
    """Example of job programation
    """

    def __init__(self, params):
        super().__init__(params)

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
        print('Parameters: ', self.parameters)
        number = self.parameters['arg1']
        number_two = self.parameters['arg2']

        self.process_data()
        r = 0
        counter = 0
        while counter < 1000:
            r += float(number) / float(number_two)
            counter += 1
        self.pulzar_add_log('Result is: ' + str(r))
        self.pulzar_set_output('Result is: ' + str(r))


def execute(arguments):
    """Point of entrance

        Parameter description
        =====================


    """
    example = Example(arguments)
    example.run_my_code()
    return example.is_the_job_ok()
