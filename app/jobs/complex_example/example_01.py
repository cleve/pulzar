from pulzarcore.core_jobs import CoreJobs
# Internal import
from .core.database import DB


class Example(CoreJobs):
    """This is a complex app, with custom modules
    and packages wrapped into Pulzar
    """

    def __init__(self, params):
        super().__init__(params)
        self.database = DB()

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        print('Parameters: ', self.parameters)
        query = self.database.execute_query('SELECT * FROM DB')
        self.pulzar_add_log(query)
        self.pulzar_set_output('Result is: ' + query)


def execute(arguments):
    """Point of entrance
    """
    example = Example(arguments)
    example.run_my_code()
    return example.is_the_job_ok()
