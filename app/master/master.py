from pulzarutils.constants import Constants
from pulzarutils.constants import Response
from pulzarutils.utils import Utils
from pulzarutils.logger import PulzarLogger
from master.dispatcher import Dispatcher
from pulzarcore.core_response import ResponseClass


class Master:
    def __init__(self):
        self.utils = Utils()
        self.logger = PulzarLogger(master=True)
        self.dispatcher = Dispatcher(self.utils, self.logger)
        self.response = ResponseClass()
        self.master_env = None

    def process_request(self, env, start_response):
        '''Master method to process all the requests
        '''
        # Get request type
        self.master_env = self.utils.extract_host_env(env)
        message = self.dispatcher.classify_request(
            self.master_env, env, start_response)
        # Get the code already included in the object
        request_type = message.code_type

        # OPTIONS requests
        if request_type == Constants.OPTIONS:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())
            return self.response.get_response(start_response, Response.OPTIONS)
        # Handle general errors
        if request_type == Constants.USER_ERROR or request_type == Constants.PULZAR_ERROR:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.SKYNET_RESTORE:
            self.response.set_response('200 OK')
            self.response.set_message(
                self.utils.py_to_json(
                    {'response': 'start_backup'}, to_bin=True)
            )

        elif request_type == Constants.SKYNET_RECORD_ADDED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.SKYNET_RECORD_RESTORED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.SKYNET_RECORD_ALREADY_ADDED:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.SKYNET:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.ADMIN:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        # If not Skynet or administrative tasks
        elif request_type == Constants.GET_NODE:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.KEY_NOT_FOUND:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.KEY_FOUND_DELETE:
            url_path = env[Constants.PATH_INFO]
            redirect_url = 'http://' + message.volume + url_path
            self.response.set_response('307 temporary redirect')
            self.response.set_redirection(redirect_url)

        elif request_type == Constants.KEY_FOUND:
            # Here redirection or negotiation
            url_path = env[Constants.PATH_INFO]
            redirect_url = 'http://' + message.volume + url_path
            self.response.set_response(message.http_code)
            self.response.set_redirection(redirect_url)

        elif request_type == Constants.REDIRECT_PUT:
            # Getting original query parameters
            query_params = self.utils.extract_query_params(
                'http://fakeurl.com?' + env['QUERY_STRING'])

            redirect_url = 'http://' + message.volume + \
                env[Constants.PATH_INFO] + '?url=' + \
                self.master_env[Constants.HTTP_HOST]
            for param in query_params:
                redirect_url += '&' + param + '=' + query_params[param][0]
            self.response.set_response(message.http_code)
            self.response.set_redirection(redirect_url)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.EXTENSION_RESPONSE:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.JOB_RESPONSE:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.JOB_DETAILS:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        elif request_type == Constants.JOB_ERROR:
            self.response.set_response(message.http_code)
            self.response.set_message(message.get_bjson())

        return self.response.get_response(start_response)
