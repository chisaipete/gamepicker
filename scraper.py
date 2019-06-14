import os

from bs4 import BeautifulSoup
from picker_lib import Game, Library

with open('hb.html') as hb:
    # this is a downloaded version of https://www.humblebundle.com/home/library
    soup = BeautifulSoup(hb, features='html.parser')
    items = soup.find_all("div", class_="text-holder")
    titles = [(type(i), i.get_text()) for i in items]
    games = Library()

    for title in titles:
        t = title[1].lower()
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
            # print(title[1].replace('Steam Key', '').replace('Origin Key', '').strip().split('\n')[0])
            games.add_game(Game(title[1].replace('Steam Key', '').replace('Origin Key', '').strip().split('\n')[0], ['humble']))
    print(f"{len(games)} of {len(items)} are games.")
    games.save_to_disk(os.path.join(os.getcwd(), 'hb.json'))
