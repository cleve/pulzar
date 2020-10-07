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
        number = 15.0
        number_two = 42000.0
        self.pulzar_add_log(
            'Number 1 = {}, Number 2 {}'.format(number, number_two))
        self.process_data()
        r = 0
        counter = 0
        while counter < 100:
            r += float(number) / float(number_two)
            self.pulzar_add_log('Current r={}'.format(r))
            counter += 1
        self.pulzar_set_output('Result is: ' + str(r))
        self.pulzar_set_output('Job done')


def execute(arguments):
    """Point of entrance

        Parameter description
        =====================


    """
    example = Example(arguments)
    example.run_my_code()
    return example.is_the_job_ok()
