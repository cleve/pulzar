import unittest
from unittest.mock import patch
from pulzarutils.utils import Constants
from unittest.mock import patch, Mock
# Object to test
from master.job_process import JobProcess


class TestJobProcess(unittest.TestCase):
    """Testing JobProcess:
        - Cancel job
    """
    
    @patch('pulzarcore.core_job_master.Job.send_job')
    @patch('pulzarcore.core_rdb.RDB.execute_sql')
    def test_process_request_cancel_job(self, mock_data_base, mock_send_job):
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

    @patch('pulzarcore.core_job_master.Job.send_job')
    @patch('pulzarcore.core_rdb.RDB.execute_sql')
    @patch('pulzarcore.core_body.Body.extract_params')
    def test_process_request_add_job(self, mock_extract, mock_data_base, mock_send_job):
        mock_extract = Mock()
        mock_extract.return_value = {'param': 1, 'job_id': 22}
        mockresponse = Mock()
        mockresponse.return_value.job_id = 22
        mock_send_job.return_value = mockresponse
        mock_response_db = Mock()
        mock_response_db.return_value = 99
        mock_logger = Mock()
        binary_obj = Mock()
        byte_string = b'{"arg": 1}'
        binary_obj.return_value.read = byte_string
        env = {
            Constants.WSGI_INPUT: binary_obj,
            Constants.CONTENT_LENGTH: str(len(byte_string)),
            Constants.CONTENT_TYPE: 'application/json'}
        query_string = 'query=string'
        job_process = JobProcess(mock_logger)
        job_return = job_process.process_request('http://localhost:31414/launch_job/dir/job_name', query_string, env)
        assert job_return.http_code == '200 OK'
        assert job_return.response.get('status') == 'ok'
        assert job_return.response.get('msg').find('Job added with id') > -1