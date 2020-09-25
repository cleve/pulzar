import pyodbc
from pulzarutils.utils import Utils


class MSSQL:
    def __init__(self, unix_string=None, windows_string=None):
        """Init config strings
        """
        self.utils = Utils()
        self.server_config = server_config
        self.windows_string = windows_string
        # Init
        self._init_cursor()

    def _init_cursor(self):
        if self.utils.is_unix():
            self.init_unix_cursor()
        else:
            self.init_windows_cursor()

    def init_unix_cursor(self):
        """Use:
            DSN=MSSQLServerDatabase;UID=myuid;PWD=mypwd
        """
        conn = pyodbc.connect(self.server_config['conn_string'])
        conn.autocommit = True
        self.cursor = conn.cursor()

    def init_windows_cursor(self, conn_string):
        """Windows connection string compatible
        """
        conn = pyodbc.connect(self.windows_string)
        conn.autocommit = True
        self.cursor = conn.cursor()

    def execute_sp(self, sp, arguments, fetch=True):
        data = self.cursor.execute(sp, arguments)
        return data.fetchall() if fetch else True

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
