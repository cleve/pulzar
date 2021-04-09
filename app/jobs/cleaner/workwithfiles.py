import tempfile
from timeit import default_timer as timer
from pulzarutils.public import Public
from pulzarcore.core_jobs import CoreJobs


class Workwithfiles(CoreJobs):
    """Work with key provided in the pulzar_data parameter

    Parse and print
    """

    def __init__(self, params):
        super().__init__(params)

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        start = timer()
        # Getting file path
        filepath = self.pulzar_get_filepath()
        if filepath is not None:
            # Opening file and parsing it.
            self.pulzar_add_log(f'filepath: {filepath}')
            with open(filepath) as f:
                # Creating a new file.
                with tempfile.NamedTemporaryFile() as fp:
                    for line in f:
                        if line is None:
                            break
                        sep = line.split(' ')
                        self.pulzar_set_output(f'Key {sep[0]} with value {sep[1]}')
                        fp.write(f'Key {sep[0]} with value {sep[1]}')
                    # Saving the file in the DB.
                    self.pulzar_store_file(fp.name, 1)
                    
        self.pulzar_set_output(f'Total time: {timer() - start}')

    def is_the_job_ok(self):
        """Should be at the end
        """
        return not self._failed_job

    def execute(self):
        '''
        Description: Using files created in the DB
        Arguments: {"pulzar_data": "key"}
        Category: Examples
        Author: Mauricio Cleveland
        '''
        self.run_my_code()
        return self.is_the_job_ok()
