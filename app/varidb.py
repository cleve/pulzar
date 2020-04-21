import sys

# Internal
from master.master import Master


def application(env, start_response):
    master = Master()
    return master.process_request(env, start_response)
