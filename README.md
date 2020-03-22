# VariDB

Intended to be used in an internal network. In the future will be added security.

VariDB is a distributed database system, with load balance, easy to recover and backup.

## Uses

* Configuration server.
* Store big amount of data, scalable.

### Start system

uwsgi --ini config/master.ini
uwsgi --ini config/volume.ini

## Dependences

* lmdb
* requests

# Methods

## String values

### Add key value
master:[port]/add_key/{key}/{value}

### Read key value
master:[port]/get_key/{key}

### Remove key value
master:[port]/delete_key/{key}

### Update key value
master:[port]/update_key/{key}/{value}

## Binary values

### Add key binary
master:[port]/add_file/{key}/{value}

### Read key value
master:[port]/get_file/{key}

### Remove key value
master:[port]/delete_file/{key}

### Update key value
master:[port]/update_file/{key}/{value}

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

master:[port]/skynet/{node_id}