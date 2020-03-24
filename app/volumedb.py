from volume.volume import Volume

def application(env, start_response):
    volume_obj = Volume()
    volume_obj.process_request(env, start_response)
    start_response('200 OK', [('Content-Type','application/json')])
    return [b"Hello World"]