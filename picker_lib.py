import os
import json
import random
import unittest
from pathlib import Path


class Distributor:
    def __init__(self, name=None, authorize=True):
        if name:
            self.name = name
        else:
            self.name = self.__class__.__name__.lower()
        self.library = Library()
        self.credentials = {}
        self.connection_alive = None
        self.api = None
        if authorize:
            self.load_credentials()
        self.setup_connection()

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

    def get_titles_from_library(self):
        return self.library.to_list()

    def add_game(self, title, played=False):
        self.library.add_game(Game(title, distributor=[self.name], played=played))

    def get_game(self, title):
        return self.library.get_game(title)

    def setup_connection(self):
        self.connection_alive = False

    def load_library_with_games(self):
        pass


class Library:
    def __init__(self):
        self.games = {}

    def __len__(self):
        return len(self.games)

    def __eq__(self, other):
        return self.games == other.games

    def to_list(self):
        return list(self.games.keys())

    def total_games(self, unplayed=False):
        if unplayed:
            return len([game for game in self.games if not self.get_game(game).played])
        else:
            return len(self.games)

    def add_game(self, game):
        if game.name in self.games:
            self.games[game.name].distributors = sorted(list(set(self.games[game.name].distributors + game.distributors)))
        else:
            self.games[game.name] = game

    def get_game(self, name):
        return self.games.get(name, None)

    def get_distributors(self):
        unique_distributors = []
        for game in self.games:
            for distributor in self.get_game(game).distributors:
                unique_distributors.append(distributor)
        return list(set(unique_distributors))

    def add_games_from_distributor(self, distributor):
        for title in distributor.get_titles_from_library():
            self.add_game(distributor.get_game(title))

    def add_games_from_distributor_list(self, distributor_list):
        for distributor in distributor_list:
            self.add_games_from_distributor(distributor)

    def save_to_disk(self, lib_file):
        with open(lib_file, 'w') as save_file:
            json.dump(self.games, save_file, cls=GameEncoder)

    def load_from_disk(self, lib_file):
        with open(lib_file, 'r') as load_file:
            self.games = json.load(load_file, object_hook=game_decoder)

    def choose_game(self):
        if len(self) == 0:
            raise LibraryIsEmptyError
        return self.get_game(random.choice(list(self.games.keys())))

    def __str__(self):
        library_string = ''
        game_list = self.to_list()

        try:
            max_game_name = max([len(self.get_game(g).name) for g in game_list])
            max_distributor_name = max([len(self.get_game(g).distributors) for g in game_list])
        except ValueError:
            max_game_name = 1
            max_distributor_name = 1

        line_string = f"{{:{max_game_name}}} | {{:{max_distributor_name}}} | {{}}\n"

        for game in game_list:
            library_string += line_string.format(game.name, game.distributors, 'X' if game.played else ' ')

        return library_string


class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Game):
            return {
                '__type__': 'Game',
                'name': obj.name,
                'distributors': obj.distributors,
                'played': obj.played
            }
        return json.JSONEncoder.default(self, obj)


def game_decoder(obj):
    if '__type__' in obj and obj['__type__'] == 'Game':
        return Game(obj['name'], obj['distributors'], obj['played'])
    return obj


class Game:
    def __init__(self, name=None, distributor=[], played=False):
        self.name = name
        self.played = played
        self.distributors = distributor

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
        self.distributor_cred_file = os.path.join(os.getcwd(), 'distributor.cred')
        with open(self.distributor_cred_file, 'w') as dcf:
            dcf.writelines("""client_id 123456789ABCDEF
client_secret ABCDEF123456789ABCDEF
token thisissomecrazystring""")
        self.distributor = Distributor()
        self.master_library = Library()

    def tearDown(self):
        os.remove(self.distributor_cred_file)

    def test_empty_library(self):
        self.assertEqual([], self.distributor.get_titles_from_library())

    def test_library_of_one_game(self):
        self.distributor.add_game('foo')
        self.assertEqual(1, len(self.distributor.get_titles_from_library()))

    def test_empty_game(self):
        game = Game()
        self.assertEqual(None, game.name)
        self.assertEqual(False, game.played)

    def test_create_game_with_name(self):
        game = Game("Foobar")
        self.assertEqual("Foobar", game.name)

    def test_create_game_with_name_and_played(self):
        game_a = Game("Foobar")
        game_b = Game("Bizwiz", played=True)
        self.assertEqual(False, game_a.played)
        self.assertEqual(True, game_b.played)

    def test_only_games_in_library(self):
        self.distributor.add_game('foo')
        self.assertIsInstance(self.distributor.get_game('foo'), Game)

    def test_distributor_has_name(self):
        self.assertEqual('distributor', self.distributor.name)
        steam = Distributor('steam')
        self.assertEqual('steam', steam.name)

    def test_distributor_loads_existing_credentials(self):
        self.assertIsNotNone(self.distributor.credentials)
        distributor_credentials = {
            'client_id': '123456789ABCDEF',
            'client_secret': 'ABCDEF123456789ABCDEF',
            'token': 'thisissomecrazystring',
        }
        self.assertEqual(distributor_credentials, self.distributor.credentials)

    def test_no_credentials_exist_on_disk(self):
        with self.assertRaises(NoCredentialFileFoundError):
            Distributor('bad_file_name')

    def test_established_connection(self):
        self.assertIsNotNone(self.distributor.connection_alive)
        self.assertFalse(self.distributor.connection_alive)
        # self.assertTrue(self.distributor.connection_alive)

    def test_master_library_exists(self):
        self.assertIsInstance(self.master_library, Library)

    def test_distributor_uses_library_object(self):
        self.assertIsInstance(self.distributor.library, Library)

    def test_master_library_distributor_list_combining_functionality(self):
        self.assertEqual(0, len(self.master_library))
        steam = Distributor('steam', False)
        gog = Distributor('gog', False)
        hb = Distributor('humble', False)
        steam.add_game('A')
        steam.add_game('B')
        gog.add_game('B')
        gog.add_game('C')
        hb.add_game('D')
        self.assertEqual(2, len(steam))
        self.assertEqual(2, len(gog))
        self.assertEqual(1, len(hb))
        self.master_library.add_games_from_distributor(steam)
        self.master_library.add_games_from_distributor(gog)
        self.master_library.add_games_from_distributor(hb)
        self.assertEqual(4, len(self.master_library))

    def test_master_library_uniquify_games_when_added(self):
        steam = Distributor()
        gog = Distributor()
        hb = Distributor()
        steam.add_game('A')
        gog.add_game('B')
        gog.add_game('C')
        hb.add_game('B')
        hb.add_game('D')
        self.master_library.add_games_from_distributor_list([steam, gog, hb])
        self.assertEqual(4, len(self.master_library))

    def test_game_object_serialization(self):
        g = Game('foo', 'bar', True)
        encoded = GameEncoder().encode(g)
        dec_g = json.loads(encoded, object_hook=game_decoder)
        self.assertEqual(g, dec_g)

    def test_save_and_load_library_to_and_from_disk(self):
        self.distributor.add_game('A')
        self.distributor.add_game('B')
        self.distributor.add_game('C')
        self.master_library.add_games_from_distributor(self.distributor)
        json_file = os.path.join(os.getcwd(), 'test.json')
        self.master_library.save_to_disk(json_file)
        self.assertTrue(os.path.exists(json_file))
        temp_library = Library()
        temp_library.load_from_disk(json_file)
        self.assertEqual(self.master_library, temp_library)
        os.remove(json_file)

    def test_choose_game_from_library(self):
        self.distributor.add_game('A')
        self.distributor.add_game('B')
        self.distributor.add_game('C')
        self.master_library.add_games_from_distributor(self.distributor)
        chosen_game = self.master_library.choose_game()
        self.assertIsInstance(chosen_game, Game)

    def test_distributor_list_is_unique(self):
        Path('1.cred').touch()
        Path('2.cred').touch()
        dist_1 = Distributor('1')
        dist_2 = Distributor('2')
        dist_1.add_game('A')
        dist_2.add_game('A')
        self.master_library.add_games_from_distributor_list([dist_1, dist_2])
        self.assertIsInstance(self.master_library.get_game('A').distributors, list)
        self.assertEqual(['1', '2'], self.master_library.get_game('A').distributors)
        os.remove('1.cred')
        os.remove('2.cred')

    def test_library_stats_functions(self):
        self.assertEqual(0, self.master_library.total_games())
        self.distributor.add_game('A')
        self.distributor.add_game('B')
        self.master_library.add_games_from_distributor(self.distributor)
        self.assertEqual(2, self.master_library.total_games())
        self.assertEqual(2, self.master_library.total_games(unplayed=True))
        self.assertEqual(1, len(self.master_library.get_distributors()))

