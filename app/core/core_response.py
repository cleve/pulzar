class Respose:
    def __init__(self):
        self.JSON = [('Content-Type','application/json')]
        self.headers = []

    def set_headers(self, header):
        self.headers.append(header)