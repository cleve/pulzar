import pyodbc
from pulzarutils.utils import Utils


class MSSQL:
    def __init__(self, server_config=None):
        """Init config strings
        """
        self.utils = Utils()
        self.server_config = server_config
        # Init
        self._init_cursor()

    def _init_cursor(self):
        if self.server_config is None:
            return
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
        conn = pyodbc.connect(self.server_config['win_conn_string'])
        conn.autocommit = True
        self.cursor = conn.cursor()

    def execute_sp(self, sp, arguments, fetch=True):
        if self.server_config is None:
            return []
        data = self.cursor.execute(sp, arguments)
        return data.fetchall() if fetch else True

    def query(self, query):
        if self.server_config is None:
            return []
        self.cursor.execute(query)
        return self.cursor.fetchall()
