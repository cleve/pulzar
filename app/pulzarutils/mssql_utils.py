import pyodbc
from pulzarutils.utils import Utils


class MSSQL:
    def __init__(self, server_config):
        self.utils = Utils()
        self.server_config = server_config
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
    
    def init_windows_cursor(self):
        conn = pyodbc.connect(
            'Driver={{SQL Server}};'
            'Server={};'
            'Database={};'
            'UID={};'
            'PWD={};'
            'Trusted_Connection=no'.format(
                self.server_config['server_name'],
                self.server_config.server_config['database'],
                self.server_config.server_config['usr'],
                self.server_config.server_config['psw']
            ) 
        )
        conn.autocommit = True
        self.cursor = conn.cursor()

    def execute_sp(self, sp, arguments, fetch=True):
        data = self.cursor.execute(sp, arguments)
        return data.fetchall() if fetch else True

    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
        
