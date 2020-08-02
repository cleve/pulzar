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

    def run_job(self):
        """Send job to be proccesed
        """
        print('Running job')

    def notification(self):
        """Notify to master
        """
        print('Sending notification...')
