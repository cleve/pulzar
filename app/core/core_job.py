# Internal imports
from core.core_request import CoreRequest
from utils.node_utils import NodeUtils
from utils.constants import ReqType


class Job:
    """Send tasks to the nodes
    """

    def __init__(self, job_path, job_name, job_params):
        self.workers = None
        self.job_path = job_path
        self.job_name = job_name
        self.job_params = job_params

    def send_job(self, const):
        """Send job to the node selected

            params:
             - const (Constants)
        """
        node_utils = NodeUtils(const)
        node = node_utils.pick_a_volume()
        print('Sending job')
        request = CoreRequest(node.decode(), '9001', '/send_job')
        request.set_type(ReqType.POST)
        request.set_payload(self.job_params)
        return request.make_request()
