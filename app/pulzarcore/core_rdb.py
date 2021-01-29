import sqlite3


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

        Parameters
        ----------
        query : str
            SQL with the query
        param : tuple , default = None

        Return
        ------
        list
            List of tuples with the results
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
            query string
        params : tuple
            Tuple with the values to insert
        
        Return
        ------
        int
            Last id or -1 if failed
        """
        try:
            self.cursor.execute(query, param)
            self.database.commit()
            return self.cursor.lastrowid
        except BaseException as err:
            return -1

    def execute_sql_update(self, query, param):
        """Update data
            return rows affected
        """
        self.cursor.execute(query, param)
        self.database.commit()
        return self.cursor.rowcount

    def close(self):
        """Close conn
        """
        self.cursor.close()
