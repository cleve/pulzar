import lmdb

class DB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.env = None
        self.init_db()

    def init_db(self):
        try:
            self.env = lmdb.open(self.db_path, max_dbs=2)
        except Exception as err:
            raise Exception("DB Class", err)

    def put_value(self, key_string):
        pass

    def get_value(self, key_string):
        pass

    def delete_value(self, key_value):
        pass