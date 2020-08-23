from pulzarutils.utils import Utils


class Messenger:
    """Base class for messages
    """

    def __init__(self):
        self.utils = Utils()
        self.volume = None
        self.code_type = 'default'
        self.http_code = '200 OK'
        self.extra = None
        self.response = {
            'response': None,
            'status': 'ok',
            'msg': ''
        }

    @property
    def set_message(self):
        """Add message into the dictionary
        """
        return self.response['msg']

    @set_message.setter
    def set_message(self, message):
        """Add message into the dictionary
        """
        self.response['msg'] = message

    def mark_as_failed(self):
        """Set the response as failed one
        """
        self.response['status'] = 'ko'

    def set_response(self, response):
        """Add response into the dictionary
        """
        self.response['response'] = response

    def get_bjson(self):
        """Get the response dictionary into JSON format
        """
        try:
            return self.utils.py_to_json(self.response).encode()
        except Exception as err:
            return self.utils.py_to_json({
                'response': 'Internal error',
                'status': 'ko',
                'msg': str(err)
            }).encode()
