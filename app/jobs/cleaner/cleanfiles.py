import base64
import requests
from timeit import default_timer as timer
from pulzarutils.public import Public
from pulzarcore.core_jobs import CoreJobs


class Cleanfiles(CoreJobs):
    """Clean files

    Delete key values
    """

    def __init__(self, params):
        super().__init__(params)
        self.public = Public()
        self.base_delete_url = 'http://mauricio-ksrd:31414/delete_key'

    @CoreJobs._pulzar_run_job
    def run_my_code(self):
        start = timer()
        for element in self.public.get_all_elements():
            key, val = element
            key_string = base64.b64decode(key).decode()
            req = requests.delete(
                url=self.base_delete_url + key_string
            )
            if req.status_code >= 200 and req.status_code < 300:
                self.pulzar_add_log(
                    'key {} deleted correctly'.format(key_string))
            else:
                self.pulzar_add_log('error deleting key {}'.format(key_string))
        self.pulzar_set_output('Total time: ' + str(timer() - start))

    def is_the_job_ok(self):
        """Should be at the end
        """
        return not self._failed_job

    def execute(self):
        '''
        Description: Delete files uploaded using the API
        Arguments: No args
        Category: Examples
        Author: Mauricio Cleveland
        '''
        self.run_my_code()
        return self.is_the_job_ok()
