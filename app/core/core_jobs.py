class CoreJobs:
    """Base class for job implementation
    """

    def __init__(self, parameters, notification=False):
        """Constructor
            arguments:
             - parameters (dict)
        """
        self.parameters = parameters
        self.notification_enabled = notification

    def process_params(self):
        for job in self.jobs_to_launch:
            args = job['job_args']
            if args != '':
                job['job_args'] = self.utils.json_to_py(args)
    
    def run_job(self):
        """Send job to be proccesed
        """
        print('Running job')

    def notification(self):
        """Notify to master
        """
        print('Sending notification...')
