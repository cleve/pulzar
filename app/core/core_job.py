from concurrent.futures import ThreadPoolExecutor

# Internal imports
from core.core_request import CoreRequest


class Job:
    """Send tasks to the nodes
    """

    def __init__(self):
        self.workers = None

    def send_job(self, node_info):
        """Send job to the node selected

            params:
             - node_info (Dict)
                {'host': str, 'port': str, params: dict , 'third_party': str}
        """
        host = node_info['host']
        port = node_info['port']
        params = node_info['params']
        print('Sending job')

    def start_job(self):
        """Starting the job
        """
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.send_job)
