from unittest import TestCase
from picker_lib import Distributor, Game
from steam import steamid, WebAPI


class Steam(Distributor):
    def __init__(self):
        super().__init__()
        self.steam_id = 0
        self.setup_connection()

    def setup_connection(self):
        self.api = WebAPI(key=self.credentials['web_api_key'])
        data = self.api.ISteamUser.ResolveVanityURL(
            vanityurl=self.credentials['user_id']
        )
        self.steam_id = data['response']['steamid']
        self.connection_alive = True

    def load_library_with_games(self):
        if self.connection_alive:
            self.library.games = {}
            # web call: get list of games, and their played status
            data = self.api.IPlayerService.GetOwnedGames(
                steamid=self.steam_id,
                include_appinfo=1,
                include_played_free_games=1,
                appids_filter=None
            )
            steam_game_list = data['response']['games']
            for game in steam_game_list:
                self.library.add_game(Game(game['name'], self.name, True if game['playtime_forever'] > 0 else False))


class FlatFileDistributorTests(TestCase):
    def setUp(self):
        self.stm = Steam()

    def test_created_steam_obj(self):
        self.assertEqual('steam', self.stm.name)

    def test_check_connection_and_get_steam_id(self):
        self.assertEqual(True, self.stm.connection_alive)
        self.assertIsNot(0, self.stm.steam_id)

    def test_load_library(self):
        self.assertEqual(0, len(self.stm.get_titles_from_library()))
        self.stm.load_library_with_games()
        self.assertIsNot(0, len(self.stm.get_titles_from_library()))
