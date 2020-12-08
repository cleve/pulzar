# Pulzar

Intended to be used in an internal network. In the future will be added security.

Pulzar has two components

### VariDB

Is a distributed database system, with load balance, easy to recover and backup.

### Job system

Is a distributed job system with load balance.

## Uses

* Configuration server.
* Store big amount of data, scalable.
* Run jobs (Python scripts in parallel).

## Dependences

### Next Python modules are needed

* lmdb
* requests
* psutil
* schedule

## Configuration

The system can be configured under **config/server.conf**

The configuration is pretty simple:

```ini
[server]
host=localhost
port=31414

[volume]
# Where to store files
dir=/var/lib/pulzar/data
port=31415

[general]
retention_policy=90

[jobs]
dir=jobs

[backup]
active=False
type=None
address=None
user=None
psw=None
```

### Start system DEV

If you are in Ubuntu, remove the default **uwsgi** package installed, and use 
**pip** to get the proper one.

Make sure to run in DEBUG mode. Under utils/constants.py

```sh
cd app
uwsgi --ini config/master.ini
uwsgi --ini config/volume.ini
```

# Methods

## String values

### Add key value

```sh
master:[port]/add_key/{key}
curl -X PUT -L -T /path/to/file http://master:[port]/add_key/{key}
```

### Add a key value during a time

Use the **temporal** parameter.

```sh
master:[port]/add_key/{key}?temporal=[int:days]
curl -X PUT -L -T /path/to/file http://master:[port]/add_key/{key}?temporal={int}
```

Where the int value indicates the amount of days than the file will be available.

For large files, you can use an efficient way:

1. Request the node URL for your key
2. Use the URL in 1 for upload the file

Example:

```sh
# Request the url
master:[port]/get_node/{key}
curl -X GET -L http://master:[port]/get_node/my_key.txt
```

Response:

```json
{
    "data": 
        {
            "node": "http://node:port/add_key/my_key.txt?url=master:port"
        },
    "status": "ok",
    "msg": "ok"
}
```

Use the **node** URL to storage the file

```sh
# Upload the file
curl -X PUT -T /path/to/file/my_key.txt -L http://master:[port]/get_node/my_key.txt
```

#### Snippets ####

##### c# #####
```csharp
// Upload the file
using (WebClient wc = new WebClient())
    {
        try
        {
            string apiUrl = @"http://master:[port]/add_key/path/my_key.key"
            wc.Headers.Add("Content-Type", "application/octet-stream");
            wc.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0");
            byte[] result = wc.UploadFile(apiUrl, "PUT", filePath);
            // Get string response, you should serialize it.
            string strResult = Encoding.UTF8.GetString(result);
        }
        catch (Exception ex)
        {
            // Handle ex.
        }
    }
```

##### Python #####

```python
# Upload the file
try:
    req = requests.put(
        url='http://master:[port]/add_key/path/my_key.key',
        data=open('path/to/the/file.key', 'rb'),
        headers={'Content-Type': 'application/octet-stream'}
    )
except Exception as err:
    # Handle error
```

### Read key value
```sh
master:[port]/get_key/{key}
curl -X GET -L http://master:[port]/get_key/{key}
```

### Remove key value
```sh
master:[port]/delete_key/{key}
curl -X DELETE -L http://master:[port]/delete_key/{key}
```

## Integrations

### Extending the app

Sometimes you would like to add your own code, like some analysis over the data
or even a totally new kind of process. This feature is intended to execute process 
during the request operation.

By default the next libaries are ready to go:

- pyodbc
- opencv
- pytesseract
- Pillow
- psycopg2

In order to do this, you can add a module into the
***app/extensions/*** directory. The extension must have a class with the
name of the file **capitalized**.

If the extension is:

```app/extensions/mysuperextension```

The class has to be named **Mysuperextension**

The template of the file:

```py
from pulzarutils.extension import Extension


class Mysuperextension(Extension):
    def __init__(self, arguments, params, file_path=None):
        '''Receiving values
            URL: http://master:[port]/extension/arg_1/arg_2/arg_n?param_1=1&param_2=2&param_n=n

        arguments
        ---------
        arguments = ['arg_1', 'arg_2', 'arg_n']

        parameters
        ----------
        params = {'param_1': [1], 'param_2': [2], 'param_n': [n]}
        '''
        pass

    def execute(self):
        '''Mandatory method

        Return
        ------
        Python serializable: list or dictionary
        '''
        return []
```

where the *arguments* parameter is a string list provided in the URL.

Also a **return** is required as python list or dictionary.

To call the custom function you can use:

```sh
master:[port]/extension/{app_id}/{args}
curl -X GET -L http://master:[port]/extension/{app_id}/{arg1}/{arg2}/{arg_n}
```

Where **app_id** is the script added into the *extensions* directory and the **arg1, arg2,...,arg_n**
is a string list of type:

```py
['arg1', 'arg2', 'arg_n']
```

#### Example

You can find an example in the **extensions** directory:

```py
# File: example.py
from pulzarutils.extension import Extension


class Example(Extension):
    def __init__(self, arguments, params, file_path=None):
        '''Receiving values
            URL: http://master:[port]/extension/arg_1/arg_2/arg_n?param_1=1&param_2=2&param_n=n

        arguments
        ---------
        arguments = ['arg_1', 'arg_2', 'arg_n']

        parameters
        ----------
        params = {'param_1': [1], 'param_2': [2], 'param_n': [n]}
        '''

        self.args = arguments
        self.params = params

    def hello(self):
        if len(self.args) > 0:
            print('Hello example with arg ', self.args)

    def method_return(self):
        return {'my_arg': self.args, 'my_params': self.params}

    def execute(self):
        '''Mandatory method
        '''
        self.hello()
        return self.method_return()
```

#### Search extension

A search utility is included in order to demonstrate the powerful of this tool.

You can search values using dates, the format is: *mm-dd-yyyy*

```sh
# Search a key
master:[port]/extension/search/[key]

# Search a key in a specific date
master:[port]/extension/search/[key]?eq=[date]

# Search a key lower and greater than
master:[port]/extension/search/[key]?lt=[date]&gt=[date]
```

#### OCR extension

Text detection and search feature

```sh
# Get text
master:[port]/extension/ocr/[image_name]
curl -X PUT -L -T /path/to/file http://master:[port]/extension/ocr/[image_name]

# Search text into the image
master:[port]/extension/ocr/[image_name]?search=text&invert=[0|1]
curl -X PUT -L -T /path/to/file http://master:[port]/extension/ocr/[image_name]?search=text&invert=[0|1]
```

Response

```json
{
    "data": {
        "text": "ubuntu\n\f"
    },
    "status": "ok",
    "msg": ""
}
```

#### Image Match extension

Search a sub-image into a base image

```sh
# Search a sub-image
master:[port]/extension/image/[image_name.extension]?image_url=[URI]
curl -X PUT -L -T /path/to/file http://master:[port]/extension/image/matching.png?image_url=[URI]

# Search a sub-image with percent
master:[port]/extension/image/[image_name.extension]?image_url=[URI]&percent=90
curl -X PUT -L -T /path/to/file http://master:[port]/extension/image/matching.png?image_url=[URI]&percent=90
```

Response

```json
{
    "data": {
        "found": true,
        "percent_of_match": 0.9,
        "coordinates": {
            "x": 242,
            "y": 32,
            "w": 800,
            "h": 409
        },
        "msg": null
    },
    "status": "ok",
    "msg": ""
}
```

## Jobs

You can launch jobs using the nodes. Similarly to third party, there is a directory 
used to store the scripts.

The job directory can be changed into the configuration file. By default 
the system is set to the **jobs** directory. 

```
app/launch_job/[custom_directory]/[your_script].py
```

The API 

```sh
# POST
master:[port]/launch_job/[custom_directory]/[your_script]
```

#### Body

```json
{
    "arg1": "value1",
    "arg2" : 123
}
```

### Scheduling jobs

To schedule a job, you need to add the *scheduled* key into the body

#### Body

```json
{
    "arg1": 12,
    "arg2": 225798,
    "scheduled": {"interval": "minutes", "time_unit": 5, "repeat": 1}
}
```

Where:

**interval**

The repetitive interval of time, this string can be:

* minutes
* hours
* weeks

**time_unit**

Indicates the repetition time based in the interval type. For example:

    interval = minutes
    time_unit = 5: 

Launch a job every 5 minutes

    interval = hours
    time_unit = 24

Launch a job every day


#### Cancel jobs

```sh
# POST
master:[port]/cancel_job/job_id
```

# Maintenance

## System information

All the API responses are formed as:

```json
{
    "data": {
        "my_data_0": 0,
        "my_data_1": 1,
        "my_data_2": "2",
        "my_data_n": [1,2]
    },
    "msg": "",
    "status": "ok",
}
```

Where the **data** key, can contain any JSON.


### Get master status

```sh
master:[port]/admin/status
curl -X GET -L http://master:[port]/admin/status
```

The response is a binding from LMDB info.

```json
data: {
    "psize": 4096,
    "depth": 2,
    "branch_pages": 1,
    "leaf_pages": 7,
    "overflow_pages": 0,
    "entries": 600
}
```

### Get network status

```sh
master:[port]/admin/network
curl -X GET -L http://master:[port]/admin/network
```

A JSON list will be sent, of type:

```json
data: [
    {
        "node": "node_name",
        "percent": 13,
        "synch": true
    }
]
```

### Get node status

```sh
master:[port]/admin/network/{node_id}
curl -X GET -L http://master:[port]/admin/network/{node_id}
```

A JSON will be sent, of type:

```json
data: {
    "node": "node_name",
    "percent": 13,
    "synch": true
}
```

### Get job status

```sh
master:[port]/admin/jobs
curl -X GET -L http://master:[port]/admin/jobs
```

A JSON will be sent, of type:

```json
data: {
    "pendings": [
        {
            "job_id": 21,
            "job_name": "example_01",
            "parameters": "{\"arg1\": \"12\", \"arg2\": \"20\"}",
            "node": "mauricio-ksrd",
            "creation_time": 0
        }
    ],
    "ready": [
        {
            "job_id": 19,
            "job_name": "example_01",
            "parameters": "{\"arg1\": \"12\", \"arg2\": \"20\"}",
            "node": "mauricio-ksrd",
            "creation_time": 1
        }
        {
            "job_id": 26,
            "job_name": "example_01",
            "parameters": "{\"arg1\": \"12\", \"arg2\": \"20\"}",
            "node": "mauricio-ksrd",
            "creation_time": 1
        }
    ],
    "failed": [
        {
            "job_id": 4,
            "job_name": "example_01",
            "parameters": "{\"arg1\": \"1\", \"arg2\": \"2\", \"arg3\": \"33\"}",
            "node": "mauricio-ksrd",
            "creation_time": 2
        },
        {
            "job_id": 5,
            "job_name": "example_01",
            "parameters": "{\"arg1\": \"1\", \"arg2\": \"2\", \"arg3\": \"33\"}",
            "node": "mauricio-ksrd",
            "creation_time": 2
        }
    ],
    "scheduled": [
        {
            "job_id": 20,
            "job_name": "example_01",
            "parameters": "{\"arg1\": 12, \"arg2\": 225798}",
            "creation_time": "2020-08-16 11:50:55.276460",
            "interval": "minutes",
            "time_unit": "5",
            "repeat": 1,
            "next_execution": "2020-08-16 14:23:53.398787"
        }
    ]
}
```

## Auto-backup

An auto-backup can be configured using the configuration file, unser the *backup* section.

## Backup

To backup the data, you only need to save the directory configured in the config file.
The example shows **/tmp/volume**. So you can simply Tar or Zip the files and move it to another 
place.

## Restore

Its pretty simple, just follow the next steps:

### Volume restauration

1. If its a fresh installation, make sure to fill up the volume configuration under **app/config**
directory. If not, go to step **2**.

2. In order to restore the files, just untar the files
previously backed into the directory configured.

3. Start the volume server

### Master restauration

1. If its a fresh installation, make sure to fill up the master configuration under **app/config**
directory.

2. Start the Master server.

3. Use *manage.py* utility to synch the volumes with the master.

```sh
python3 manage.py --restore [volume_url]
```

# Internal methods

Used internally to sync

```sh
master:[port]/skynet/
volume:[port]/autodiscovery/
```

# Dev

To run the DB locally, point your name machine properly to 127.0.0.1 in the 
**/etc/hosts** file.

In order to debug faster, I created an app to view values from LMDB. This app runs over Java 11.

https://github.com/cleve/lmdb-viewer

## Keys

Keys will be encoded in base64, only ASCII chars are allowed.

## Docker

### Master

```sh
# From the root directory
docker build --rm -f dockers/Dockerfile.main -t pulzar-master:latest .

# Run it
docker run --hostname [host] --name [name] --rm -d -p 31414:31414 pulzar-master:latest
```

### Volume

```sh
# From the root directory
docker build --rm -f dockers/Dockerfile.node -t pulzar-node:latest .

# Run it
docker run --hostname [host] --name [name] --rm -d -p 31415:31415 pulzar-node:latest
```

# Test

For test purposes files of 1kb were used.

## Write tests

### Synchronical executions

For a set of 10000 instances

* Request time: 0.24316366999999997(s)
* Total time: 0.2599792804300023(s)

## Read tests

### Synchronical executions

* Request time: 0.16126144000000003(s)
* Total time: 0.17557080925000265(s)

## Delete tests

* Request time: 0.17187763999999994
* Total time: 0.26895125860000463

## Restore test

Preparing 600 files: 23.977071480000177(s)

## Windows

You can use the linux subsystem. Tested with Ubuntu 20.04.

First install pip3 using

```sh
sudo apt install python3-pip
```

After, install **uwsgi** with pip3

```sh
 sudo pip3 install uwsgi
```

# Test docker in local

You can try with the public repo on dockerhub:

```sh
# Run UI
docker run -it --name pulzar-ui -d --rm -p 80:80 mauriciocleveland/pulzar-ui:1.0.1

# Run master
docker run ---network host --name pulzar-master --rm -d -p 31414:31414 mauriciocleveland/pulzar-master:1.0.1

# Run node
docker run ---network host --name pulzar-node --rm -d -p 31415:31415 mauriciocleveland/pulzar-node:1.0.1
```