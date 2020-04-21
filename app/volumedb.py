from volume.volume import Volume


def application(env, start_response):
    volume_obj = Volume()
    return volume_obj.process_request(env, start_response)
