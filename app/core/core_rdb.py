import sqlite3


class RDB:
    """Relational DB package
    """

    def __init__(self, db_path):
        self.database = sqlite3.connect(db_path)
        self.cursor = self.database.cursor()

    def execute_sql(self, query):
        self.cursor.execute(query)
        self.cursor.commit()

    def close(self):
        self.cursor.close()
