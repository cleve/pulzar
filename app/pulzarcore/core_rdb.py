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
        """
        if param is None:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_sql_insert(self, query, param):
        """Insert data
            return ID (int)
        """
        self.cursor.execute(query, param)
        self.database.commit()
        return self.cursor.lastrowid

    def close(self):
        """Close conn
        """
        self.cursor.close()
