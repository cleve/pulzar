import sys

# Internal
from master.master import Master 

def application(env, start_response):
    print (env)
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]