import logging
import re

from utils.mongo_utils import MongoUtils


class Search:
    def __init__(self, mongo_connection_string):
        self._db = MongoUtils.setup_connection(mongo_connection_string)

    def start_search(self):
        """
        Start receiving input from user and running the search and print the results
        """
        print('Welcome to Hadar\'s Search System.')
        print('if you want to exit enter: -1')
        print('Enter your first word/s for search: ')
        user_input = input().lower()

        while user_input != '-1':
            user_input = re.findall(r"(?<![@#])\b\w+(?:'\w+)?", user_input)

            if not user_input:
                print('Please enter words and not signs for search:')
                user_input = input().lower()

                continue

            results = self._search_in_db(user_input)

            if results is None:
                print('No results found.')
            else:
                print('Search results:\n', results)

            print('Enter -1 if you want to exit or your next word/s for search: ')
            user_input = input().lower()

        print('Thank you for using Hadar\'s Search System')

    def _search_in_db(self, search_words_list):
        """
        Searches for the given words in the database and sort them by joint appearances and by frequency
        :param search_words_list: list of words to search
        :return: results
        """
        logging.debug('Searching for the words {}'.format(search_words_list))
        db_results = {result['word']: result for result in self._db.words.find({'word': {'$in': search_words_list}})}
        result_count = len(db_results)
        logging.debug('Found result for {}/{} words'.format(len(db_results), len(search_words_list)))

        if result_count == 0:
            return None

        elif result_count == 1:
            results = {}
            for file, result in db_results[list(db_results.keys())[0]]['appearances'].items():
                results[file] = result['frequency']

            results = sorted(results, key=results.get, reverse=True)
            logging.debug('Found {} files that have the words {}'.format(len(results), search_words_list))

            return results

        joint_file_names, disjoint_file_names = self._get_joint_and_disjoint_file_names(db_results)
        results = self._find_matches_in_joint_files(joint_file_names, search_words_list, db_results)
        logging.debug('found {}/{} files with match for all words'.format(len(results), len(joint_file_names)))
        results = sorted(results, key=results.get, reverse=True)

        return results + disjoint_file_names

    def _get_joint_and_disjoint_file_names(self, db_results):
        """
        Split the db results into files that match all words and those that do not
        :param db_results: The results for the words from database
        :return: joint_file_names, disjoint_file_names
        """
        joint_file_names = set(db_results[list(db_results.keys())[0]]['appearances'])
        disjoint_file_names = {}

        for word, result in db_results.items():
            joint_file_names.intersection_update(result['appearances'])

            for file in result['appearances']:
                if file in joint_file_names:
                    continue

                if file not in disjoint_file_names:
                    disjoint_file_names[file] = 0

                disjoint_file_names[file] += result['appearances'][file]['frequency']

        disjoint_file_names = sorted(disjoint_file_names, key=disjoint_file_names.get, reverse=True)
        logging.debug('Found {} intersecting files and {} disjoint'.format(len(joint_file_names),
                                                                           len(disjoint_file_names)))
        return joint_file_names, disjoint_file_names

    def _find_matches_in_joint_files(self, joint_file_names, search_words_list, db_results):
        """
        Find matches for all words in the joint files
        :param joint_file_names: List of joint file names
        :param search_words_list: List of words searched
        :param db_results: The results of the search from the database
        :return: results
        """
        results = {}

        for file in joint_file_names:
            success_positions = []
            first_word = search_words_list[0]

            for position in db_results[first_word]['appearances'][file]['positions']:
                success = False

                for index_word in range(1, len(search_words_list)):
                    if position + index_word not in \
                            db_results[search_words_list[index_word]]['appearances'][file]['positions']:
                        success = False

                        break
                    else:
                        success = True

                if success:
                    success_positions.append(position)

            if success_positions:
                logging.debug(
                    'Found {} positions that match all search words in file {}'.format(len(success_positions), file))
                results[file] = len(success_positions)

        return results
