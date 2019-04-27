import os
from unittest import TestCase
from picker_lib import Distributor, Library, Game


class JsonDistributor(Distributor):
    def load_credentials(self):
        pass

    def load_library_with_games(self, path=None):
        if path:
            self.library.games = {}
            self.library.load_from_disk(path)
            for game in self.library.games:
                self.library.games[game].distributors = self.name


class FlatFileDistributorTests(TestCase):
    def setUp(self):
        self.test_library = Library()
        self.test_library.add_game(Game('Risk of Rain 2'))
        self.test_library.add_game(Game('Mortal Kombat 11'))
        self.test_library.add_game(Game('Imperator: Rome'))
        self.test_library.add_game(Game('MONSTER HUNTER: WORLD'))
        self.test_library.add_game(Game('Forager'))
        self.json_lib = os.path.join(os.getcwd(), 'ff.json')
        self.test_library.save_to_disk(self.json_lib)

    def tearDown(self):
        os.remove(self.json_lib)

    def test_created_ff_obj(self):
        jd = JsonDistributor()
        self.assertEqual('jsondistributor', jd.name)

    def test_load_library(self):
        jd = JsonDistributor()
        self.assertEqual(0, len(jd.get_titles_from_library()))
        jd.load_library_with_games(self.json_lib)
        self.assertEqual(5, len(jd.get_titles_from_library()))
        for game in jd.get_titles_from_library():
            self.assertEqual(jd.name, jd.get_game(game).distributors)
