import argparse

from dist_json import JsonDistributor
from dist_steam import Steam
from picker_lib import Library, LibraryIsEmptyError

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Master PC Game Library & Picker!')
    parser.add_argument('-r', '--read_library', help="echo the Master Library stats to the console",
                        action='store_true', default=False)
    parser.add_argument('-p', '--pick_game', help="select an unplayed game at random, echo to console",
                        action='store_true', default=False)
    args = parser.parse_args()

    # load master library from list of registered distributors
    ml = Library()

    steam = Steam()
    steam.load_library_with_games()
    hb = JsonDistributor('humblebundle')
    hb.load_library_with_games('hb.json')
    gog = JsonDistributor('gog')
    gog.load_library_with_games('gog.json')

    ml.add_games_from_distributor(steam)
    ml.add_games_from_distributor(hb)


    if args.read_library:
        # print(ml)
        print(f"Master Library: {ml.total_games()} games, {ml.total_games(unplayed=True)} unplayed, across these platforms: {' '.join(ml.get_distributors())}")

    if args.pick_game:
        try:
            chosen_game = ml.choose_game()
            print(f"You should play: {chosen_game.name} on {chosen_game.distributors}")
        except LibraryIsEmptyError:
            print(f"Sad. You have no games to choose from!")
