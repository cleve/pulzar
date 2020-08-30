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


def reset():
    """Delete all the data
    """
    pass


def main():
    """Entrance point
    """
    arg_parse = argparse.ArgumentParser(
        prog='manage', description='Manage DB')
    arg_parse.add_argument(
        '--restore',
        metavar='volume URL',
        action='store',
        type=str,
        required=True
    )

    arg_parse.add_argument(
        '--backup',
        metavar='volume URL',
        action='store',
        type=str,
        required=True
    )

    arg_parse.add_argument(
        '--reset',
        metavar='',
        action='store',
        type=str,
        required=True
    )

    args = arg_parse.parse_args()

    if args.restore:
        restore(args.restore)

    if args.reset:
        reset(args.restore)


if __name__ == "__main__":
    main()
