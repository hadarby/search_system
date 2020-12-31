import pymongo
import logging


class MongoUtils:
    @staticmethod
    def setup_connection(connection_string, database_name='search_system'):
        """
        Set up the connection to mongodb
        :param connection_string: The connection string
        :param database_name: The name of the database to use
        """
        try:
            client = pymongo.MongoClient(connection_string)
            db = client[database_name]
            logging.info('Connected to mongodb')

            return db
        except Exception as ex:
            raise Exception('Received an exception while trying to setup mongo connection - {}'.format(ex))
