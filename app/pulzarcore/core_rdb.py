import sqlite3
from typing import Final


class RDB:
    """Relational DB package
    """

    def __init__(self, db_path):
        self.database = sqlite3.connect(db_path)
        self.cursor = self.database.cursor()

    def execute_sql(self, query):
        """Generic query
            return int: rows affected
        """
        self.cursor.execute(query)
        self.database.commit()
        return self.cursor.rowcount

    def execute_sql_with_results(self, query, param=None):
        """Execute query and return iterator
        """
        if param is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, param)
        return self.cursor.fetchall()

    def execute_sql_insert(self, query, param):
        """Insert data

        Parameters
        ----------
        query : str
            query string to be exectuted
        params : tuple
            parameters
        
        Return
        ------
        int
            Last row inserted
        """
        self.cursor.execute(query, param)
        self.database.commit()
        return self.cursor.lastrowid

    def execute_sql_update(self, query, param):
        """Update data

        Parameters
        ----------
        query : str
            Query to be executed with placeholder
        param : tuple
            Tuple with de values specified in the query
        
        Return
        ------
        int
            Rows affected
        """
        self.cursor.execute(query, param)
        self.database.commit()
        return self.cursor.rowcount

    def secuential_executions(self, executions):
        """Multiple executions

        Parameters
        ----------
        executions : iterator
            string iterator
        
        Return
        ------
        bool
            True if the operations were correct
        """
        try:
            for sql in executions:
                self.cursor.execute(sql)
            
            self.database.commit()
            return True
        except BaseException as err:
            return False

    def close(self):
        """Close conn
        """
        self.cursor.close()
