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
        message = self.dispatcher.classify_request(
            self.master_env, env, start_response)
        # Get the code already included in the object
        request_type = message.code_type

        # Handle general errors
        if request_type == self.const.USER_ERROR or request_type == self.const.PULZAR_ERROR:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.SKYNET_RESTORE:
            self.response.set_response('200 OK')
            self.response.set_message(
                self.utils.py_to_json(
                    {'response': 'start_backup'}, to_bin=True)
            )

        elif request_type == self.const.SKYNET_RECORD_ADDED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.SKYNET_RECORD_RESTORED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.SKYNET_RECORD_ALREADY_ADDED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.SKYNET:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.ADMIN:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        # If not Skynet or administrative tasks
        elif request_type == self.const.KEY_NOT_FOUND:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.KEY_FOUND_DELETE:
            url_path = env[self.const.PATH_INFO]
            redirect_url = 'http://' + message.volume + url_path
            self.response.set_response('307 temporary redirect')
            self.response.set_redirection(redirect_url)

        elif request_type == self.const.KEY_FOUND:
            # Here redirection or negotiation
            url_path = env[self.const.PATH_INFO]
            redirect_url = 'http://' + message.volume + url_path
            self.response.set_response(message.http_code)
            self.response.set_redirection(redirect_url)

        elif request_type == self.const.REDIRECT_PUT:
            # Getting original query parameters
            query_params = self.utils.extract_query_params(
                'http://fakeurl.com?' + env['QUERY_STRING'])

            redirect_url = 'http://' + message.volume + ':9001' + \
                env[self.const.PATH_INFO] + '?url=' + \
                self.master_env[self.const.HTTP_HOST]
            for param in query_params:
                redirect_url += '&' + param + '=' + query_params[param][0]
            self.response.set_response(message.http_code)
            self.response.set_redirection(redirect_url)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.TP_RESPONSE:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.JOB_RESPONSE:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == self.const.JOB_ERROR:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        return self.response.get_response(start_response)
