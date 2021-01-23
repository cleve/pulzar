import requests
import tempfile
import random
import string
from timeit import default_timer as timer
from concurrent.futures import ThreadPoolExecutor

TEST_CASES = 100
THREAD = 5
MASTER_URL = 'http://127.0.0.1:31414/extension/ocr/'
IMG = 'data/text_example.png'

thread_pool = ThreadPoolExecutor(max_workers=THREAD)

for instance_test in range(TEST_CASES):
    req = requests.put(
        url=MASTER_URL + 'ocr_image.png',
        data=open(IMG, 'rb'),
        headers={'Content-Type': 'application/octet-stream'}
    )
    print(req.json()['status'])
