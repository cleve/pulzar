import sys

# Internal
from master.master import Master 

def application(env, start_response):
    master = Master()
    print(env)
    master.process_request(env, start_response)
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]