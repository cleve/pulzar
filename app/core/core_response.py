class Respose:
    def __init__(self):
        self.JSON = ('Content-Type','application/json')
        self.headers = []

    def set_headers(self, header):
        """Add headers to the response
        Parameters
            header: tuple(key, value)
        Return
            void
        """
        self.headers.append(header)