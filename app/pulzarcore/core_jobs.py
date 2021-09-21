from abc import abstractmethod
from abc import ABCMeta
from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.file_utils import FileUtils
from pulzarutils.node_utils import NodeUtils
from pulzarutils.constants import ReqType
from pulzarutils.stream import Config
from pulzarcore.core_rdb import RDB
from pulzarcore.core_request import CoreRequest
from pulzarcore.core_rabbit import Rabbit


class CoreJobs(metaclass=ABCMeta):
    """Base class for job implementation

    To test locally, set the attribute local_exec = True
    The method **execute** is mandatory
    
    """

    def __init__(self, parameters, notification=False):
        """Constructor

        Parameters
        ----------
        parameters : dict
            Dictionary with parameters to be used.
        
        notification : bool
            True to send notifications

        """
        # Allows to execute the job locally
        self.local_exec = False
        self._pulzar_utils = Utils()
        self.pulzar_parameters = parameters
        # Emails or push
        self._notification_enabled = notification
        self._job_id = parameters.get('job_id')
        self._start_time = self._pulzar_utils.get_current_datetime()
        self._log = []
        self._failed_job = False
        self._pulzar_job_output = []
        self._pulzar_data_file_path = None
        self._pulzar_config = parameters.get('_pulzar_config')

        # log
        self._pulzar_register_parameters()
        self._pulzar_get_data()

        # Publisher to master for finished jobs
        self.rabbit_notify = Rabbit('notify_jobs_ready')

    @abstractmethod
    def execute(self):
        '''Entrance for extensios
        '''
        return

    @property
    def pulzar_output(self):
        if self.local_exec:
            print(f'-> Output')
            for line in self._pulzar_job_output:
                print(line)
        else:
            return self._pulzar_job_output

    @pulzar_output.setter
    def pulzar_output(self, output):
        self._pulzar_job_output.append(output)

    @property
    def pulzar_log(self):
        """Pretty print for logs

        This method print line by line the logs
        """
        if self.local_exec:
            print(f'-> Logs')
            for line in self._log:
                print(line)
        else:
            return self._log

    @pulzar_log.setter
    def pulzar_log(self, log):
        self._log.append(log)

    def pulzar_set_output(self, output_str):
        """Write output

        Parameters
        ----------
        output_str: String
        """
        self._pulzar_job_output.append(output_str)

    def pulzar_add_log(self, message, bulk=False):
        """With bulk=True, a list of string is allowed
        """
        if bulk and isinstance(message, list):
            self._log += message
        self._log.append(message)

    def pulzar_print_output(self):
        """Pretty print for logs

        This method print line by line the logs
        """
        for line in self._pulzar_job_output:
            print(line)
    
    def pulzar_store_file(self, file_name, temporary=90):
        """Method used to create files in the system.
        
        The file will be stored in the same node and
        a new record will be created in the master.

        Parameters
        ----------
        file_name : str
            Name of the file to create

        temporary : int, default=90
            Set a temporary value in days
            in which the file will be stored.

        Return
        ------
        bool
            True if the file was created
        """
        if self.local_exec:
            print('Local debug is active::pulzar_store_file is not working')
            return False
        file_utils = FileUtils()
        server_config = Config(Constants.CONF_PATH)
        node_utils = NodeUtils()
        node = node_utils.discover_volume()
        # Master url
        server_host = server_config.get_config('server', 'host')
        server_port = server_config.get_config('server', 'port')
        base_dir = '/jobs'
        if self._pulzar_config['scheduled']:
            base_dir += '/sheduled/' + str(self._job_id)
        else:
            base_dir += '/regular/' + str(self._job_id)
        file_utils.set_path(base_dir)
        full_key = base_dir + '/' + \
            self._pulzar_utils.get_base_name_from_file(file_name)
        # File creation
        base64_str = self._pulzar_utils.encode_base_64(
            full_key, True)
        # Trying to create the key-value
        key_to_binary = self._pulzar_utils.encode_str_to_byte(base64_str)
        file_utils.set_key(key_to_binary, base64_str)
        file_utils.read_binary_local_file(file_name)
        request_object = CoreRequest(
            server_host, server_port, Constants.ADD_RECORD)
        request_object.set_type(ReqType.POST)
        request_object.set_path(Constants.ADD_RECORD)
        # We have to send the key, volume and port.
        request_object.set_payload({
            'key': file_utils.get_key(),
            'volume': node,
            'temporal': temporary
        })
        if not request_object.make_request():
            # If an error ocurr in the server, we need to delete the file.
            file_utils.remove_file()
            return False
        self.pulzar_add_log('FILE: ' + file_utils.get_decoded_key())
        return True

    def _pulzar_get_data(self):
        """Check file/config and assign it
        """
        file_path = self.pulzar_parameters.get('pulzar_data')
        if file_path is not None:
            parent_dir = self._pulzar_utils.get_parent_name_from_file(
                file_path
            )
            abs_path = self._pulzar_utils.get_absolute_path_of_dir() + '/' \
                + Constants.DATA_DIR + '/' \
                + parent_dir + '/' \
                + self._pulzar_utils.encode_base_64(
                    file_path, to_str=True)
            
            if self._pulzar_utils.file_exists(abs_path):
                self._pulzar_data_file_path = abs_path
            else:
                # File not found
                self.pulzar_add_log(f'WARNING: path {abs_path} not found in the node')
                self._pulzar_data_file_path = None

    def pulzar_get_filepath(self):
        """Return filepath
        """
        return self._pulzar_data_file_path

    def _pulzar_register_parameters(self):
        """Add parameters into the log register
        """
        if self.pulzar_parameters:
            self.pulzar_add_log(
                self._pulzar_utils.py_to_json(self.pulzar_parameters)
            )
    
    def _pulzar_run_job(executor):
        """Decorator to handle job execution
        """
        def wrapper(self):
            print('Pulzar core executing')
            try:
                executor(self)
            except Exception as err:
                self._mark_as_failed()
                self.pulzar_add_log('PULZAR_ERROR::' + str(err))
            self._pulzar_notification()
            return self.is_the_job_ok()
        return wrapper

    def is_the_job_ok(self):
        """Should be at the end
        """
        return not self._failed_job

    def _mark_as_failed(self):
        """Mark the job as failed
        """
        self._failed_job = True
    
    def _pulzar_notification(self):
        """Notify to master, use message broker
        """
        if self.local_exec:
            return
        end_time = self._pulzar_utils.get_current_datetime()
        delta = end_time - self._start_time
        # Formating logs
        final_log = '\n'.join(self._log)
        final_output = '\n'.join(self._pulzar_job_output)
        # Notify to master
        self.rabbit_notify.publish(
            (
                f'NOTIFY_JOB,{self._job_id},{final_log},{final_output},'
                f'{delta.total_seconds()},{1 if self.is_the_job_ok() else 2},'
                f'{self._notification_enabled},{self._pulzar_config.get("scheduled",0)}')
            )
        # Notifications
        if self._notification_enabled:
            print('Sending notification...')
