from pulzarcore.core_jobs import CoreJobs


class Example(CoreJobs):
    """This is a complex app, with custom modules
    and packages wrapped into Pulzar
    """

    def __init__(self, params):
        super().__init__(params)


def execute(arguments):
    """Point of entrance
    """
    example = Example(arguments)
    # example.run_my_code()
    return example.is_the_job_ok()
