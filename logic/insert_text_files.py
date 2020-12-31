import logging
import os
import re

from tqdm import tqdm

from utils.mongo_utils import MongoUtils


class TextFiles:
    def __init__(self, mongo_connection_string, folder_name='../lyrics/'):
        self._folder_name = folder_name
        self._db = MongoUtils.setup_connection(mongo_connection_string)

    def start(self):
        """
        Insert all the words in user folder to our database
        """
        logging.info('Starting insertion of text files')
        self._setup_words_collection()
        file_to_words = self._split_files_into_words()

        with tqdm(total=len(file_to_words), desc='Inserting files', bar_format='{l_bar}{bar} [ time left: {remaining} ]') as file_bar:
            for file in file_to_words:
                logging.info('Inserting file {} to mongodb'.format(file))
                words_to_appearances = self._format_data(file_to_words[file], file)

                with tqdm(total=len(words_to_appearances), desc='Inserting words from file {}'.format(file),
                          bar_format='{l_bar}{bar} [ time left: {remaining} ]') as words_bar:
                    for word in words_to_appearances:
                        word_exist = self._db.words.find_one({'word': {'$in': ['{}'.format(word)]}})

                        if word_exist is None:
                            self._db.words.insert_one({'word': '{}'.format(word),
                                                       'appearances':
                                                           {file: {'positions': words_to_appearances[word]['appearances'][file],
                                                                   'frequency':
                                                                       len(words_to_appearances[word]['appearances'][file])}}})
                        else:
                            self._db.words.update_one({'word': '{}'.format(word)}, [{'$set': {
                                'appearances': {file: {'positions':  words_to_appearances[word]['appearances'][file],
                                                'frequency': len(words_to_appearances[word]['appearances'][file])}}}}])
                        words_bar.update(1)
                        
                file_bar.update(1)
                logging.info('Successfully inserted file {} to mongodb'.format(file))

        logging.info('Successfully saved {} files to mongodb'.format(len(file_to_words)))

    def _setup_words_collection(self):
        """
        Set up the words collection in mongodb
        """
        logging.info('Setting up \'words\' collection')
        self._db.words.drop()
        self._db.create_collection('words')
        self._db.words.create_index([('word', 1), ('appearances', 1)], unique=True)
        logging.info('Successfully set up \'words\' collection')

    def _split_files_into_words(self):
        """
        Split all files into words
        :return: file_to_words
        """
        file_to_words = {}

        for file in os.listdir(self._folder_name):
            with open(os.path.join(self._folder_name, file), 'r') as f:
                file_name = file[:-4]
                file_to_words[file_name] = re.findall(r"(?<![@#])\b\w+(?:'\w+)?", f.read().lower())

        logging.info('Split {} files to words'.format(len(file_to_words)))

        return file_to_words

    def _format_data(self, words_list, file_name):
        """
        Create the right format remember - index from 0 and position from 1
        :param words_list: list of words
        :param file_name: name of the file
        :return: words_to_appearances
        """
        words_to_appearances = {}

        for index in range(len(words_list)):
            word = words_list[index]

            if word not in words_to_appearances.keys():
                words_to_appearances[word] = {'word': word, 'appearances': {file_name: []}}

            words_to_appearances[word]['appearances'][file_name].append(index+1)

        return words_to_appearances





