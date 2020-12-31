import logging

from logic.search import Search
from utils.logging_utils import LoggingUtils


def main():
    try:
        LoggingUtils.setup_logs(logging.DEBUG)
        mongo_connection_string = ''
        search = Search(mongo_connection_string)
        search.start_search()
    except SystemExit:
        logging.info('Search was shut down')
    except Exception as ex:
        logging.info('Exception while searching - {}'.format(ex))


if __name__ == '__main__':
    main()
