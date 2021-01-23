import requests
import tempfile
import random
import string
from timeit import default_timer as timer
from concurrent.futures import ThreadPoolExecutor

TEST_CASES = 10000
THREAD = 5
MASTER_URL = 'http://127.0.0.1:31414/'
VOLUME_URL = 'http://127.0.0.1:31415/'

thread_pool_write = ThreadPoolExecutor(max_workers=THREAD)
thread_pool_read = ThreadPoolExecutor(max_workers=THREAD)
thread_pool_delete = ThreadPoolExecutor(max_workers=THREAD)
keys = []
time_request = []
time_register = []
time_errors = []

# Binary files to upload tests
binary_data = {
    '_img.jpg': 'data/wallpaper.jpg',
    '_medals.csv': 'data/downloaded_medals.csv',
    '_text_file.txt': None
}


def get_random_text(string_lenght):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=string_lenght))

def evaluate_time(report_name):
    if len(time_request) > 0:
        print('{}: Good cases {} request time with average of {}'.format(
            report_name, len(time_request), sum(time_request)/len(time_request)))
        print('{}: Good cases {} total time with average of {}'.format(
            report_name, len(time_register), sum(time_register)/len(time_register)))

    if len(time_errors) > 0:
        print('{}: Bad cases {} total time with average of {}'.format(
            report_name, len(time_errors), sum(time_errors)/len(time_errors)))

def futures_write():
    results = []
    for _ in range(TEST_CASES):
        # key creation
        key = get_random_text(10)
        # key name
        dict_key = random.choice(list(binary_data))
        url = MASTER_URL + 'add_key/test_data/' + key + dict_key + '?temporal=1'
        if dict_key == '_text_file.txt':
            # File creation or binary selection
            thread_pool_write.submit(write_test, url, results, dict_key, key, 'File')
            
        else:
            thread_pool_write.submit(write_test, url, results, dict_key, key, 'Regular')

    thread_pool_write.shutdown(wait=True)    
    return results

def futures_delete(results):
    for key in results:
        url = MASTER_URL + 'delete_key/test_data/' + key
        thread_pool_delete.submit(delete_test, url)
    thread_pool_delete.shutdown(wait=True)

def futures_read(results):
    for key in results:
        url = MASTER_URL + 'get_key/test_data/' + key
        thread_pool_read.submit(read_test, url)
    thread_pool_read.shutdown(wait=True)

def write_test(url, result_list, dict_key, key, test_type='File'):
    if test_type == 'File':
        # File creation or binary selection
        with tempfile.TemporaryFile() as tmp:
            tmp.write(get_random_text(1000).encode())
            tmp.seek(0)
            start = timer()
            req = requests.put(
                url=url,
                data=tmp,
            )
    else:
        start = timer()
        req = requests.put(
            url=url,
            data=open(binary_data[dict_key], 'rb'),
            headers={'Content-Type': 'application/octet-stream'}
        )

    if req.status_code == 201:
        time_register.append(timer() - start)
        time_request.append(req.elapsed.total_seconds())
        result_list.append(key + dict_key)
    else:
        time_errors.append(timer() - start)

def read_test(url):
    time_request = []
    time_register = []
    time_errors = []
    start = timer()
    req = requests.get(url=url)
    if req.status_code >= 200 and req.status_code < 300:
        time_register.append(timer() - start)
        time_request.append(req.elapsed.total_seconds())
    else:
        time_errors.append(timer() - start)

def delete_test(url):
    time_request = []
    time_register = []
    time_errors = []
    start = timer()
    req = requests.delete(url=url)
    if req.status_code >= 200 and req.status_code < 300:
        time_register.append(timer() - start)
        time_request.append(req.elapsed.total_seconds())
    else:
        time_errors.append(timer() - start)

results = futures_write()
evaluate_time('Write')
futures_read(results)
evaluate_time('Read')
futures_delete(results)
evaluate_time('Delete')

# start_read_test()
# start_delete_test()
