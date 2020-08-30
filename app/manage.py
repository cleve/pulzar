import argparse

# Internal imports
from pulzarcore.core_request import CoreRequest
from pulzarutils.constants import Constants
from pulzarutils.stream import Config


def restore(url):
    """Start restauration given an url
    """
    const = Constants()
    config = Config(const.CONF_PATH)
    volume_port = config.get_config('volume', 'port')
    core_request = CoreRequest(url, volume_port, '/admin/' + const.START_BK)
    if core_request.make_request() is not True:
        print('Error processing the task')
        return

    print('Starting retauration...')
    print(core_request.response)


def reset(reset):
    """Delete all the data
    """
    print('reset')
    pass


def main():
    """Entrance point
    """
    arg_parse = argparse.ArgumentParser(
        prog='manage', description='Manage Pulzar')
    arg_parse.add_argument(
        '--restore',
        metavar='volume URL',
        action='store',
        type=str,
        required=False
    )

    arg_parse.add_argument(
        '--backup',
        metavar='volume URL',
        action='store',
        type=str,
        required=False
    )
    # Delete DEV environment
    arg_parse.add_argument(
        '--reset',
        metavar='all',
        action='store',
        type=str,
        default='all',
        required=False,
        help='Restore default data for dev'
    )

    args = arg_parse.parse_args()

    if args.restore:
        restore(args.restore)

    if args.reset:
        reset(args.reset)


if __name__ == "__main__":
    main()
