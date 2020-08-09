from pulzarutils.constants import Constants
from pulzarutils.utils import Utils
from master.dispatcher import Dispatcher
from pulzarcore.core_response import ResponseClass


class Master:
    def __init__(self):
        self.const = Constants()
        self.utils = Utils()
        self.dispatcher = Dispatcher(self.utils)
        self.response = ResponseClass()
        self.master_env = None

    def process_request(self, env, start_response):
        # Get request type
        self.master_env = self.utils.extract_host_env(env)
        request = self.dispatcher.classify_request(
            self.master_env, env, start_response)
        request_type = request['action']
        print(request)

        if request_type == self.const.SKYNET_RESTORE:
            self.response.set_response('200 OK')
            self.response.set_message(
                self.utils.py_to_json(
                    {'response': 'start_backup'}, to_bin=True)
            )

        if request_type == self.const.SKYNET_RECORD_ADDED:
            self.response.set_response('200 OK')
            self.response.set_message(b'ok')

        if request_type == self.const.SKYNET_RECORD_RESTORED:
            self.response.set_response('200 OK')
            self.response.set_message(
                self.utils.py_to_json({'response': {'msg': 'ok'}}, to_bin=True)
            )
        if request_type == self.const.SKYNET_RECORD_ALREADY_ADDED:
            self.response.set_response('406 Not acceptable')
            self.response.set_message(b'already created')

        if request_type == self.const.SKYNET:
            self.response.set_response('200 OK')
            self.response.set_message(
                self.utils.py_to_json(
                    {'response': {'synch': request['parameters']}}, to_bin=True)
            )
        if request_type == self.const.ADMIN:
            self.response.set_response('200 OK')
            self.response.set_message(request['parameters'])

        # If not Skynet or administrative tasks
        if request_type == self.const.KEY_NOT_FOUND:
            self.response.set_response('200 OK')
            self.response.set_message(b'key not found')

        if request_type == self.const.KEY_FOUND_DELETE:
            url_path = env[self.const.PATH_INFO]
            if request['volume'] is None:
                self.response.set_response('203 No Content')
                self.response.set_message(
                    b'There is not volumes registered or online')
            else:
                redirect_url = 'http://' + request['volume'] + url_path
                self.response.set_response('307 temporary redirect')
                self.response.set_redirection(redirect_url)

        if request_type == self.const.KEY_FOUND:
            # Here redirection or negotiation
            url_path = env[self.const.PATH_INFO]
            if request['volume'] is None:
                self.response.set_response('203 No Content')
                self.response.set_message(
                    b'There is not volumes registered or online')
            else:
                redirect_url = 'http://' + self.utils.decode_byte_to_str(
                    request['volume']) + url_path
                self.response.set_response('307 temporary redirect')
                self.response.set_redirection(redirect_url)

        if request_type == self.const.REDIRECT_POST:
            if request['volume'] is None:
                self.response.set_response('203 No Content')
                self.response.set_message(
                    b'There is not volumes registered or online')
            else:
                # Getting original query parameters
                query_params = self.utils.extract_query_params(
                    'http://fakeurl.com?' + env['QUERY_STRING'])

                redirect_url = 'http://' + self.utils.decode_byte_to_str(
                    request['volume']) + ':9001' + env[self.const.PATH_INFO] + '?url=' + self.master_env[self.const.HTTP_HOST]
                for param in query_params:
                    redirect_url += '&' + param + '=' + query_params[param][0]
                self.response.set_response('307 temporary redirect')
                self.response.set_redirection(redirect_url)
                self.response.set_message(b'ok')

        if request_type == self.const.TP_RESPONSE:
            self.response.set_response('200 OK')
            self.response.set_message(request['parameters'])

        if request_type == self.const.JOB_RESPONSE:
            self.response.set_response('200 OK')
            self.response.set_message(request['parameters'])

        if request_type == self.const.JOB_ERROR:
            self.response.set_response('200 OK')
            self.response.set_message(b'error launching job')

        return self.response.get_response(start_response)
