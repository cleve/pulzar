import sqlite3


class RDB:
    """Relational DB package
    """

    def __init__(self, *args, **kwargs):
        self.db = None
