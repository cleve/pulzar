from pulzarutils.utils import Utils
from pulzarutils.utils import Constants
from pulzarutils.messenger import Messenger
from pulzarcore.core_rdb import RDB
from pulzarcore.core_job_master import Job
from pulzarcore.core_body import Body


class JobProcess:
    """Main class to handle jobs
    """

    def __init__(self, logger):
        self.TAG = self.__class__.__name__
        self.logger = logger
        self.utils = Utils()
        self.data_base = RDB(Constants.DB_JOBS)
        self.messenger = Messenger()

    def process_request(self, url_path, query_string, env):
        """Entry point. Processing job request
        """
        params = {}
        try:
            # Add or cancel
            # cancel
            job_path = self.utils.get_search_regex(
                url_path,
                Constants.RE_CANCEL_JOB
            )
            if job_path is not None:
                # Canceling job
                job_id = job_path.groups()[0]
                sql = 'UPDATE schedule_job SET scheduled = -2 WHERE job_id = {}'.format(
                    job_id
                )
                update_rows_affected = self.data_base.execute_sql(sql)
                if update_rows_affected == 0:
                    self.messenger.code_type = Constants.JOB_ERROR
                    self.messenger.mark_as_failed()
                    return self.messenger
                self.messenger.code_type = Constants.JOB_RESPONSE
                self.messenger.set_message = 'Job canceled with id ' + \
                    str(job_id)
                return self.messenger

            job_path = self.utils.get_search_regex(
                url_path,
                Constants.RE_LAUNCH_JOB
            )
            # parameters to send to a node
            job_path, job_name = job_path.groups()
            body = Body()
            job_params = body.extract_params(env)
            params['job_path'] = job_path
            params['job_name'] = job_name
            params['job_id'] = None
            params['parameters'] = job_params
            full_path = job_path + '/' + job_name
            job_object = Job(params, full_path, self.logger)
            
            if job_object.send_job():
                self.messenger.code_type = Constants.JOB_RESPONSE
                self.messenger.set_message = 'Job added with id ' + \
                    str(job_object.job_id)

            else:
                self.messenger.set_message = job_object.error_msg
                self.messenger.code_type = Constants.JOB_ERROR
                self.messenger.mark_as_failed()

        except Exception as err:
            self.logger.exception(':{}:{}'.format(self.TAG, err))
            self.messenger.code_type = Constants.JOB_ERROR
            self.messenger.mark_as_failed()
            self.messenger.set_message = str(err)

        return self.messenger
