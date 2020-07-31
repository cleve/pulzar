import sqlite3


class RDB:
    """Relational DB package
    """

    def __init__(self, db_path):
        self.database = sqlite3.connect(db_path)
        self.cursor = self.database.cursor()

    def execute_sql_with_params(self, query, param):
        self.cursor.execute(query, param)
        self.database.commit()

    def close(self):
        self.cursor.close()
