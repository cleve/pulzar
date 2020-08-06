import time
from pulzarcore.core_jobs import CoreJobs


class Example(CoreJobs):
    """Example of job programation
    """

    def __init__(self, params):
        super().__init__(params)

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        print('Parameters: ', self.parameters, type(self.parameters))
        number = self.parameters['arg1']
        number_two = self.parameters['arg2']
        time.sleep(1)
        r = number / number_two
        self.pulzar_add_log('Result is: ' + str(r))


def execute(arguments):
    """Point of entrance
    """
    example = Example(arguments)
    example.run_my_code()
    return example.is_the_job_ok()
