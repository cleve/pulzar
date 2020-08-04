import time
from pulzarcore.core_jobs import CoreJobs


class Example(CoreJobs):
    """Example of job programation
    """

    def __init__(self, params):
        super().__init__(params)

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        time.sleep(20)
        r = 1.0/10.0
        self.pulzar_add_log('Result is: ' + str(r))


def execute(arguments):
    """Point of entrance
    """
    example = Example(arguments)
    example.run_my_code()
    return example.is_the_job_ok()
