import time
from pulzarcore.core_jobs import CoreJobs


class Example(CoreJobs):
    """Example of job programation
    """

    def __init__(self, params):
        super().__init__(params)

    def run_job(self):
        try:
            time.sleep(10)
            r = 1/0
            return True
        except Exception as err:
            self.mark_as_failed()
            self.add_log(str(err))

        return False


def execute(arguments):
    """Point of entrance
    """
    example = Example(arguments)
    example.run_job()
    example.notification()
    return example.is_the_job_ok()
