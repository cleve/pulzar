import time
from pulzarcore.core_jobs import CoreJobs


class Example(CoreJobs):
    """Example of job programation
    """

    def __init__(self, params):
        print(params)

    def run_job(self):
        time.sleep(10)


def execute(arguments):
    """Point of entrance
    """
    example = Example(arguments)
    example.run_job()
