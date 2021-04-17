from pulzarcore.core_jobs import CoreJobs
# Internal import
from .core.database import DB


class Example01(CoreJobs):
    """This is a complex app, with custom modules
    and packages wrapped into Pulzar
    """

    def __init__(self, params):
        super().__init__(params)
        self.database = DB()

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        print('Parameters: ', self.pulzar_parameters)
        query = self.database.execute_query('SELECT * FROM DB')
        self.pulzar_add_log(query)

    def execute(self):
        '''
        Description: Testing with arguments
        Arguments: {"arg_1": "int", "arg_2": "str"} 
        Category: Examples
        Author: Mauricio Cleveland
        '''
        self.run_my_code()

if __name__ == '__main__':
    example = Example01({"arg_1": "1", "arg_2": "some string"})
    example.local_exec = True
    example.execute()
    # Print logs
    example.pulzar_log

    # Print output
    example.pulzar_output
