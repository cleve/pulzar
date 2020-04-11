import sys

# Internal
from master.master import Master


def application(env, start_response):
    master = Master()
    return master.process_request(env, start_response)
    # start_response('200 OK', [('Content-Type','text/html')])
    # start_response('302 permanent redirect', [('Content-Type','text/html'), ('Location', 'http://www.kuasard.com')])
