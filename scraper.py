import os
import io
import argparse

from bs4 import BeautifulSoup
from picker_lib import Game, Library

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--service', help='service to scrape downloaded html [hb, gog]')
    args = parser.parse_args()

    if args.service == 'hb':
        with open('hb.html') as hb:
            # this is a downloaded version of https://www.humblebundle.com/home/library
            soup = BeautifulSoup(hb, features='html.parser')
            items = soup.find_all("div", class_="text-holder")
            titles = [i.get_text() for i in items]
            games = Library()

            for title in titles:
                t = title.lower()
                if '% off' in t or \
                        'boss fight books' in t or \
                        'frog god games' in t or \
                        'lone shark games' in t or \
                        'black scrolls games' in t or \
                        'skybound' in t or \
                        'narrated' in t or \
                        'cross promotion' in t or \
                        'soundtrack' in t or \
                        'no starch press' in t or \
                        '3d-printcraft.net' in t or \
                        'o\'reilly' in t or \
                        'pyxel edit' in t or \
                        'hobgoblin3d' in t or \
                        'user manual' in t or \
                        'readme' in t or \
                        'exploration guide' in t or \
                        'eula\'s' in t or \
                        '(gog)' in t or \
                        '(steam)' in t or \
                        'wiley' in t or \
                        'iain lovecraft' in t or \
                        'source code' in t or \
                        'doctorow' in t or \
                        'blinkworks' in t or \
                        'humble bundle' in t or \
                        'module' in t or \
                        'concept art' in t or \
                        'dragonlock' in t or \
                        'studio pro' in t or \
                        'double fine adventure' in t or \
                        'ben prunty' in t or \
                        'dynamite entertainment' in t or \
                        'christopher tin' in t or \
                        'art of cyan' in t or \
                        'idw publishing' in t or \
                        'neil gaiman' in t:
                    pass
                else:
                    # print(title)
                    # print(title.replace('Steam Key', '').replace('Origin Key', '').strip().split('\n')[0])
                    games.add_game(Game(title.replace('Steam Key', '').replace('Origin Key', '').strip().split('\n')[0], ['humble']))
            print(f"{len(games)} of {len(items)} are games.")
            games.save_to_disk(os.path.join(os.getcwd(), 'hb.json'))

    elif args.service == 'gog':
        with io.open('gog.html', mode='r', encoding='utf-8') as gog:
            # this is a downloaded version of https://www.gog.com/u/<username>/games
            soup = BeautifulSoup(gog, features='html.parser')
            items = soup.find_all("a", class_="prof-game__link")
            titles = [(i.h1.get_text(), True if i.aside.get_text().strip().split('\xa0')[-1] != 'Played' else False) for i in items]
            games = Library()

            for title in titles:
                name = ' '.join(title[0].replace(u"\u2122", '').replace("®", '').strip().split())
                played = title[1]
                print(f"{name}>>{played}<<")
                # print(title[1].replace('Steam Key', '').replace('Origin Key', '').strip().split('\n')[0])
                games.add_game(Game(name, ['gog']))
            print(f"{len(games)} of {len(items)} are games.")
            games.save_to_disk(os.path.join(os.getcwd(), 'gog.json'))

    elif args.service == 'epic':
        pass

    elif args.service == 'twitch':
        pass

    elif args.service == 'ubisoft':
        pass

    elif args.service == 'trove':
        pass

    elif args.service == 'bethesda':
        pass

    elif args.service == 'blizzard':
        pass
