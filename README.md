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
host=127.0.0.1
port=9000

[volume]
# Where to store files
dir=/tmp/volume
port=9001
```

Where *backup_chunk* is the amount of register to be synchronized in the backup mode.

### Start system

If you are in Ubuntu, remove the default **uwsgi** package installed, and use 
**pip** to get the proper one.

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

In order to do this, you can add a module into the
***app/third_party/*** directory. There is only one mandatory function to be added:

```py
def execute(arguments):
    example = Example(arguments[0])
    example.hello()
    return json.dumps([])
```

where the *arguments* parameter is a string list provided in the URL.

Also a **return** is required as JSON response.

To call the custom function you can use:

```sh
master:[port]/third_party/{app_id}/{args}
curl -X GET -L http://master:[port]/third_party/{app_id}/{arg1}/{arg2}/{arg_n}
```

Where **app_id** is the script added into the *third_party* directory and the **arg1, arg2,...,arg_n**
is a string list of type:

```py
['arg1', 'arg2', 'arg_n']
```

#### Example

You can find an example in the **third_party** directory:

```py
# File: example.py
import json

class Example:
    def __init__(self, arg1):
        self.arg1 = arg1
    
    def hello(self):
        print('Hello example with arg ', self.arg1)
    
    def json_return(self):
        return json.dumps({'my_arg': self.arg1})

def execute(arguments):
    example = Example(arguments[0])
    example.hello()
    return example.json_return()
```

#### Search extension

A search utility is included in order to demonstrate the powerful of this tool.

You can search values using dates, the format is: *mm-dd-yyyy*

```sh
# Search a key
master:[port]/third_party/search/[key]

# Search a key in a specific date
master:[port]/third_party/search/[key]?eq=[date]

# Search a key lower and greater than
master:[port]/third_party/search/[key]?lt=[date]&gt=[date]
```

## Jobs

You can launch jobs using the nodes. Similarly to third party, there is a directory 
used to store the scripts.

```
app/jobs/[custom_directory]/[your_script].py
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

# Maintenance

## System information

### Get master status

```sh
master:[port]/admin/status
curl -X GET -L http://master:[port]/admin/status
```

The response is a binding from LMDB info.

```json
{
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
[
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
{
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
{
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
docker build --rm -f dockers/DockerfileMaster -t varidb_master:latest .
```

### Volume

```sh
# From the root directory
docker build --rm -f dockers/DockerfileVolume -t varidb_volume:latest .
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
