import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from pulzarutils.utils import Constants
from pulzarutils.utils import Utils
from pulzarutils.node_utils import NodeUtils
from unittest.mock import patch, Mock


# Object to test
from master.job_process import JobProcess


class TestJobProcess(unittest.TestCase):
    """Testing JobProcess:
        - Cancel job
    """
    
    @patch('pulzarcore.core_job_master.Job.send_job')
    @patch('pulzarcore.core_rdb.RDB.execute_sql')
    def test_process_request(self, mock_data_base, mock_send_job):
        mockresponse = Mock()
        mock_send_job.return_value = mockresponse
        mock_response_db = Mock()
        mock_response_db.return_value = 99
        mock_logger = Mock()
        env = {Constants.CONTENT_LENGTH: '44'}
        query_string = 'query=string'
        job_process = JobProcess(mock_logger)
        job_return = job_process.process_request('http://localhost:31414/cancel_job/1', query_string, env)
        assert job_return.http_code == '200 OK'
        assert job_return.response.get('status') == 'ok'
        assert job_return.response.get('msg') == 'Job canceled with id 1'
        