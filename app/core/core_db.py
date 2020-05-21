import lmdb


class DB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.env = None
        self.init_db()

    def init_db(self):
        try:
            self.env = lmdb.open(self.db_path)
        except Exception as err:
            raise Exception("DB Class", err)

    def put_value(self, key_string, value):
        with self.env.begin(write=True) as txn:
            if not txn.get(key_string):
                txn.put(key_string, value)
                return True
            return False

    def get_value(self, key_string, to_str=False):
        with self.env.begin(write=False) as txn:
            return txn.get(key_string) if not to_str else txn.get(key_string).decode()
    
    def get_equal_value(self, key_string, value):
        with self.env.begin(write=False) as txn:
            return txn.get(key_string) == value

    def delete_value(self, key_string):
        with self.env.begin(write=True) as txn:
            if txn.get(key_string):
                txn.delete(key_string)
                return True
        return False

    def update_value(self, key_string, value):
        with self.env.begin(write=True) as txn:
            if txn.get(key_string):
                txn.put(key_string, value)

    def update_or_insert_value(self, key_string, value):
        with self.env.begin(write=True) as txn:
            txn.put(key_string, value)

    def get_values(self):
        with self.env.begin() as txn:
            return [value for _, value in txn.cursor()]

    def get_keys(self):
        with self.env.begin() as txn:
            return [key for key, _ in txn.cursor()]

    def get_keys_values(self, to_str=False):
        with self.env.begin() as txn:
            if to_str:
                return [[key.decode(), val.decode()] for key, val in txn.cursor()]
            return [[key, val] for key, val in txn.cursor()]

    def count_values(self, value, split=None):
        value = value.decode()
        counter = 0
        with self.env.begin() as txn:
            for _, val in txn.cursor():
                if value == val.decode().split(split)[0]:
                    counter += 1
            return counter