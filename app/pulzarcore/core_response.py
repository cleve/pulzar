from pulzarutils.constants import Response


class ResponseClass:
    def __init__(self):
        self.JSON = ('Content-Type', 'application/json')
        self.CORS = ('Access-Control-Allow-Origin', '*')
        self.METHODS = ('Access-Control-Allow-Methods',
                        'GET,HEAD,OPTIONS,POST,PUT')
        self.OPTIONS = ('Access-Control-Allow-Headers',
                        'Origin, X-Requested-With, Content-Type, Accept')
        self.headers = []
        self.message = b''
        self.response_code = None

    def set_message(self, message):
        self.message = message

    def set_redirection(self, site):
        self.headers.append(('Location', site))

    def set_response(self, response):
        """string with code
        """
        if response is None:
            print('Response will be override')
        self.response_code = response

    def set_headers(self, header):
        """Add headers to the response
        Parameters
            header: tuple(key, value)
        Return
            void
        """
        self.headers.append(header)

    def get_response(self, start_response, request_type=Response.JSON):
        # Cors enabled
        self.headers.append(self.CORS)
        self.headers.append(self.METHODS)
        if request_type == Response.OPTIONS:
            self.headers.append(self.OPTIONS)
        if request_type == Response.JSON:
            self.headers.append(self.JSON)
        start_response(
            self.response_code, self.headers)
        return[self.message]
