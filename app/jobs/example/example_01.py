from core.core_jobs import CoreJobs


class Example(CoreJobs):
    """Example of job programation
    """

    def __init__(self, params):
        super().__init__(self, params)


def execute(arguments):
    """Point of entrance
    """
    example = Example(arguments[0])
    example.run_job()
