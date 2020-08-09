import requests
import tempfile
import random
import string
from timeit import default_timer as timer

TEST_CASES = 100
THREAD = 1
MASTER_URL = 'http://mauricio-ksrd:9000/'
VOLUME_URL = 'http://mauricio-ksrd:9001/'

keys = []


def get_random_text(string_lenght):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=string_lenght))


def start_write_test():
    print('====== Write tests ======')
    time_request = []
    time_register = []
    time_errors = []
    for _ in range(TEST_CASES):
        # key creation
        key = get_random_text(10)
        # File creation
        with tempfile.TemporaryFile() as tmp:
            tmp.write(get_random_text(1000).encode())
            tmp.seek(0)
            start = timer()
            req = requests.put(
                url=MASTER_URL + 'add_key/' + key,
                data=tmp,

            )
            if req.status_code == 201:
                time_register.append(timer() - start)
                time_request.append(req.elapsed.total_seconds())
                keys.append(key)
            else:
                time_errors.append(timer() - start)

    if len(time_request) > 0:
        print('Good cases {} request time with average of {}'.format(
            len(time_request), sum(time_request)/len(time_request)))
        print('Good cases {} total time with average of {}'.format(
            len(time_register), sum(time_register)/len(time_register)))

    if len(time_errors) > 0:
        print('Bad cases {} total time with average of {}'.format(
            len(time_errors), sum(time_errors)/len(time_errors)))


def start_read_test():
    print('====== Read tests ======')
    time_request = []
    time_register = []
    time_errors = []
    for key in keys:
        start = timer()
        req = requests.get(
            url=MASTER_URL + 'get_key/' + key
        )
        if req.status_code >= 200 and req.status_code < 300:
            time_register.append(timer() - start)
            time_request.append(req.elapsed.total_seconds())
        else:
            time_errors.append(timer() - start)

    if len(time_request) > 0:
        print('Good cases {} request time with average of {}'.format(
            len(time_request), sum(time_request)/len(time_request)))
        print('Good cases {} total time with average of {}'.format(
            len(time_register), sum(time_register)/len(time_register)))

    if len(time_errors) > 0:
        print('Bad cases {} total time with average of {}'.format(
            len(time_errors), sum(time_errors)/len(time_errors)))


def start_delete_test():
    print('====== Delete tests ======')
    time_request = []
    time_register = []
    time_errors = []
    for key in keys:
        start = timer()
        req = requests.delete(
            url=MASTER_URL + 'delete_key/' + key
        )
        if req.status_code >= 200 and req.status_code < 300:
            time_register.append(timer() - start)
            time_request.append(req.elapsed.total_seconds())
        else:
            time_errors.append(timer() - start)

    if len(time_request) > 0:
        print('Good cases {} request time with average of {}'.format(
            len(time_request), sum(time_request)/len(time_request)))
        print('Good cases {} total time with average of {}'.format(
            len(time_register), sum(time_register)/len(time_register)))

    if len(time_errors) > 0:
        print('Bad cases {} total time with average of {}'.format(
            len(time_errors), sum(time_errors)/len(time_errors)))


start_write_test()
start_read_test()
start_delete_test()
