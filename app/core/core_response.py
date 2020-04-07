from utils.constants import Response


class Respose:
    def __init__(self):
        self.JSON = [('Content-Type', 'application/json')]
        self.headers = []

    def set_headers(self, header):
        self.headers.append(header)

    def get_response(self, start_response, type=Response.JSON):
        return start_response(
            '302 permanent redirect', [('Content-Type', 'text/html'), ('Location', 'http://www.kuasard.com')])
