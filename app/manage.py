import argparse

# Internal imports
from pulzarcore.core_request import CoreRequest
from pulzarutils.constants import Constants
from pulzarutils.stream import Config
from pulzarutils.utils import Utils


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

    print('Starting restauration...')
    print(core_request.response)


def reset(reset):
    """Delete all the data
    """
    utils = Utils()
    const = Constants()
    # Only delete dev directories
    const.DEBUG = True

    def delete_db(path_dir):
        data_files = utils.get_all_files(path_dir + '/**')
        for item in data_files:
            print('Cleaning => ', item)
            if item == path_dir + '/' or item.find('gitignore') >= 0:
                continue
            utils.remove_file(item)
        if path_dir.find(const.DEV_DIRECTORY) >= 0:
            return
        utils.remove_dir(path_dir)

    if reset == 'all':
        delete_db(const.DB_PATH)
        delete_db(const.DB_VOLUME)
        delete_db(const.DB_NOT_PERMANENT)
        delete_db(const.DB_STATS)
        delete_db(const.DB_BACKUP)
        delete_db(const.DEV_DIRECTORY)

        # TODO: RDB
    print('Done')


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

    elif args.reset:
        reset(args.reset)


if __name__ == "__main__":
    main()
