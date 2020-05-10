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
```

### Start system

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
curl -X POST -L -T /path/to/file http://master:[port]/add_key/{key}
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
        "percent": 13
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
    "percent": 13
}
```

## Backup

## Restore

# Internal methods

Used internally to sync

```sh
master:[port]/skynet/
volume:[port]/autodiscovery
```

# Dev

To run the DB locally, point your name machine properly to 127.0.0.1 in the 
**/etc/hosts** file.

## Keys

Keys will be encoded in base64, only ASCII chars are allowed.