import os
import pickle
import random
import unittest


class Distributor:
    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__.lower()
        self.library = Library()
        self.credentials = {}
        self.connection_alive = None
        self.load_credentials()
        self.check_connection()

    def __len__(self):
        return len(self.library)

    def load_credentials(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        cred_file_path = os.path.join(basedir, '.'.join([self.name, 'cred']))

        if not os.path.exists(cred_file_path):
            raise NoCredentialFileFoundError

        with open(cred_file_path) as cred_file:
            for line in cred_file.readlines():
                if line:
                    key, value = line.split()
                    self.credentials[key] = value

    def get_library(self):
        return self.library.to_list()

    def add_game(self, title):
        self.library.append(Game(title))

    def check_connection(self):
        self.connection_alive = False


class Library:
    def __init__(self):
        self.games = []

    def __len__(self):
        return len(self.games)

    def __eq__(self, other):
        return self.games == other.games

    def to_list(self):
        return self.games

    def append(self, title):
        self.games.append(title)

    def add_games_from_distributor(self, distributor):
        for game in distributor.get_library():
            self.games.append(game)

    def add_games_from_distributor_list(self, distributor_list):
        for distributor in distributor_list:
            for game in distributor.get_library():
                self.games.append(game)

    def save_to_disk(self, lib_file):
        with open(lib_file, 'wb') as save_file:
            pickle.dump(self.games, save_file)

    def load_from_disk(self, lib_file):
        with open(lib_file, 'rb') as load_file:
            self.games = pickle.load(load_file)

    def choose_game(self):
        if len(self) == 0:
            raise LibraryIsEmptyError
        return random.choice(self.games)


class Game:
    def __init__(self, name=None, played=False):
        self.name = name
        self.played = played

    def __eq__(self, other):
        return self.name == other.name and self.played == other.played


class NoCredentialFileFoundError(Exception):
    """Raised when a file for storing credentials for a distributor is not found"""
    pass


class LibraryIsEmptyError(Exception):
    """Raised when trying to choose a game from an empty library"""
    pass


class DistributorTests(unittest.TestCase):

    def setUp(self):
        self.distributor = Distributor()
        self.master_library = Library()

    def test_empty_library(self):
        self.assertEqual([], self.distributor.get_library())

    def test_library_of_one_game(self):
        self.distributor.add_game(Game())
        self.assertEqual(1, len(self.distributor.get_library()))

    def test_empty_game(self):
        game = Game()
        self.assertEqual(None, game.name)
        self.assertEqual(False, game.played)

    def test_create_game_with_name(self):
        game = Game("Foobar")
        self.assertEqual("Foobar", game.name)

    def test_create_game_with_name_and_played(self):
        game_a = Game("Foobar")
        game_b = Game("Bizwiz", True)
        self.assertEqual(False, game_a.played)
        self.assertEqual(True, game_b.played)

    def test_only_games_in_library(self):
        self.distributor.add_game('Foo')
        self.assertIsInstance(self.distributor.get_library()[0], Game)

    def test_distributor_has_name(self):
        self.assertEqual('distributor', self.distributor.name)

    def test_distributor_loads_existing_credentials(self):
        self.assertIsNotNone(self.distributor.credentials)
        distributor_credentials = {
            'client_id': '123456789ABCDEF',
            'client_secret': 'ABCDEF123456789ABCDEF',
            'token': 'thisissomecrazystring',
        }
        self.assertEquals(distributor_credentials, self.distributor.credentials)

    def test_no_credentials_exist_on_disk(self):
        with self.assertRaises(NoCredentialFileFoundError):
            bad_distributor = Distributor('bad_file_name')

    def test_established_connection(self):
        self.assertIsNotNone(self.distributor.connection_alive)
        self.assertFalse(self.distributor.connection_alive)
        # self.assertTrue(self.distributor.connection_alive)

    def test_master_library_exists(self):
        self.assertIsInstance(self.master_library, Library)

    def test_distributor_uses_library_object(self):
        self.assertIsInstance(self.distributor.library, Library)

    def test_master_library_distributor_list_combining_functionality(self):
        self.assertEquals(0, len(self.master_library))
        steam = Distributor()
        steam.add_game('A')
        gog = Distributor()
        gog.add_game('B')
        gog.add_game('C')
        hb = Distributor()
        hb.add_game('D')
        self.assertEqual(1, len(steam))
        self.assertEqual(2, len(gog))
        self.assertEqual(1, len(hb))
        self.master_library.add_games_from_distributor(steam)
        self.master_library.add_games_from_distributor(gog)
        self.master_library.add_games_from_distributor(hb)
        self.assertEqual(4, len(self.master_library))
        self.master_library.add_games_from_distributor_list([gog, gog, gog])
        self.assertEqual(10, len(self.master_library))

    def test_save_and_load_library_to_and_from_disk(self):
        self.distributor.add_game('A')
        self.distributor.add_game('B')
        self.distributor.add_game('C')
        self.master_library.add_games_from_distributor(self.distributor)
        lib_file = os.path.join(os.getcwd(), 'test.lib')
        self.master_library.save_to_disk(lib_file)
        self.assertTrue(os.path.exists(lib_file))
        temp_library = Library()
        temp_library.load_from_disk(lib_file)
        self.assertEqual(self.master_library, temp_library)
        os.remove(lib_file)

    def test_choose_game_from_library(self):
        self.distributor.add_game('A')
        self.distributor.add_game('B')
        self.distributor.add_game('C')
        self.master_library.add_games_from_distributor(self.distributor)
        chosen_game = self.master_library.choose_game()
        self.assertIsInstance(chosen_game, Game)


if __name__ == '__main__':
    unittest.main()
