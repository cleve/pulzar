from pulzarutils.utils import Utils


class HttpResponse:
    """Base class for Json responses
    """

    def __init__(self):
        self.utils = Utils()
        self.response = {
            'response': None,
            'status': 'ok',
            'msg': ''
        }

    def set_response(self, response):
        """Add response into the dictionary
        """
        self.response['response'] = response

    def get_json(self):
        """Get the response dictionary into JSON format
        """
        try:
            return self.utils.py_to_json(self.response)
        except Exception as err:
            return self.utils.py_to_json({
                'response': 'Internal error',
                'status': 'ko',
                'msg': str(err)
            })
