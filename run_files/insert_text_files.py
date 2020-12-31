import logging

from logic.insert_text_files import TextFiles
from utils.logging_utils import LoggingUtils


def main():
    try:
        LoggingUtils.setup_logs(logging.INFO)
        mongo_connection_string = ''
        text_files = TextFiles(mongo_connection_string)
        text_files.start()
    except SystemExit:
        logging.info('File processing was shut down')
    except Exception as ex:
        logging.info('Exception while processing files - {}'.format(ex))


if __name__ == '__main__':
    main()
