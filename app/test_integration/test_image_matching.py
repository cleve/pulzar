import requests
import tempfile
import random
import string
from timeit import default_timer as timer
from concurrent.futures import ThreadPoolExecutor

TEST_CASES = 100
THREAD = 5
MASTER_URL = 'http://127.0.0.1:31414/'
UPLOAD_IMAGE_PATH = 'extension/imagematching?image_url='
IMG = 'data/spotify.png'

thread_pool = ThreadPoolExecutor(max_workers=THREAD)

# First upload the image
req_upload = requests.put(
    url=MASTER_URL + 'add_key/base_image_matching_test.png',
    data=open('data/image_base.png', 'rb'),
    headers={'Content-Type': 'application/octet-stream'}
)

url = req_upload.json()['data']['url']

for instance_test in range(TEST_CASES):
    req = requests.put(
        url=MASTER_URL + UPLOAD_IMAGE_PATH + MASTER_URL + url,
        data=open(IMG, 'rb'),
        headers={'Content-Type': 'application/octet-stream'}
    )
    print(req.json()['status'])

req_upload = requests.delete(
    url=MASTER_URL + 'delete_key/base_image_matching_test.png'
)