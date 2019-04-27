import argparse

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

    if args.read_library:
        print(ml)
        print(f"Master Library: {ml.total_games()} games, {ml.total_games(unplayed=True)} unplayed, across these platforms: {' '.join(ml.get_distributors())}")

    if args.pick_game:
        try:
            chosen_game = ml.choose_game()
            print(f"You should play: {chosen_game.name} on {chosen_game.distributor}")
        except LibraryIsEmptyError:
            print(f"Sad. You have no games to choose from!")
