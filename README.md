# VariDB

Intended to be used in an internal network. In the future will be added security.

VariDB is a distributed database system, with load balance, easy to recover and backup.

## Uses

* Configuration server.
* Store big amount of data, scalable.

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
backup_chunk=200
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

## Dependences

### Next Python modules are needed

* lmdb
* requests
* psutil

# Methods

## String values

### Add key value

```sh
master:[port]/add_key/{key}
curl -X PUT -L -T /path/to/file http://master:[port]/add_key/{key}
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
or even a totally new kind of process. In order to do this, you can add a module into the
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

3. Wait 10 mins, the volumes will synch automatically.

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
