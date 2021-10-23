from os import environ
from pulzarutils.constants import Constants
from pulzarutils.stream import Config

if not Constants.DEBUG:
    environ['PULZAR_MASTER_URL'] = 'pulzar-master'
    environ['PULZAR_NODE_URL'] = 'pulzar-node'
else:
    config = Config(Constants.CONF_PATH)
    environ['PULZAR_MASTER_URL'] = config.get_config('server', 'host')
    environ['PULZAR_NODE_URL'] = config.get_config('server', 'host')
