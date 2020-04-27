# VariDB

Intended to be used in an internal network. In the future will be added security.

VariDB is a distributed database system, with load balance, easy to recover and backup.

## Uses

* Configuration server.
* Store big amount of data, scalable.

### Start system

```sh
cd app
uwsgi --ini config/master.ini
uwsgi --ini config/volume.ini
```

## Dependences

* lmdb
* requests

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

### Update key value
master:[port]/update_key/{key}/{value}

## Integrations

### Custom app
master:[port]/third party/{app_id}/{value}

# Maintenance

## System information

### Get network status
master:[port]/admin/network

### Get node status
master:[port]/admin/network/{node_id}

## Backup

## Restore

# Internal methods

Used internally to sync

master:[port]/skynet/

# Dev

To run the DB locally, point your name machine properly to 127.0.0.1 in the 
**/etc/hosts** file.

## Keys

Keys will be encoded in base64, only ASCII chars are allowed.