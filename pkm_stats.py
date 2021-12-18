import requests
import math
from bs4 import BeautifulSoup

pokeapi_url = 'https://pokeapi.co/api/v2/'
pikalytics_url = "https://www.pikalytics.com/pokedex/bdspbfd/"


def open_request(url):
    r = requests.get(url)
    if r.status_code:
        return BeautifulSoup(r.text, "html.parser")
    else:
        print("page not found")


def get_all_pokemon():
    r = requests.get(pokeapi_url + 'pokemon?limit=1118')
    if r.status_code:
        names = []
        for pokemon in r.json()['results']: names.append(pokemon['name'])
        return names
    else:
        print("couldn't get pokemon information")


def get_all_natures():
    r = requests.get(pokeapi_url + 'nature')
    if r.status_code:
        natures = []
        for nature in r.json()['results']: natures.append(nature['name'])
        natures.sort()
        return natures
    else:
        print("couldn't get pokemon information")


def get_most_used():
    soup = open_request(pikalytics_url)
    pokemon_data = soup.find(id='min_list')
    names = []
    for pokemon in pokemon_data.findChildren('a', limit=2):
        names.append(pokemon.get('data-name').lower())
    return names


def split_evs(string):
    return string.split('/')


def get_pokemon_spreads(name):
    spreads = {"nature": list(), "evs": list()}
    url = pikalytics_url + name
    soup = open_request(url)
    data = soup.find("div", {"id": "dex_spreads_wrapper"}).find_all("div", {"class": "pokedex-move-entry-new"}, limit=1)
    for x in data:
        spreads["nature"].append(x.text.splitlines()[1])
        spreads["evs"].append(x.text.splitlines()[2])
    return spreads


def get_pokemon_stats(name):
    r = requests.get(pokeapi_url + 'pokemon/' + name)
    if r.status_code:
        pokemon = dict()
        pokemon['stats'] = r.json()['stats']
        pokemon['type'] = r.json()['types']
        return pokemon
    else:
        print("couldn't get pokemon information")


def get_nature(name):
    increased = ''
    decreased = ''

    r = requests.get(pokeapi_url + 'nature/' + name)
    if r.status_code:
        try:
            increased = r.json()['increased_stat']['name']
            decreased = r.json()['decreased_stat']['name']
        except Exception as e:
            print(e, flush=True)
    else:
        print("couldn't get pokemon information")
    return increased, decreased


def nature_calc(nature, stat):
    increased, decreased = get_nature(nature)

    if increased == stat:
        return 1.1
    if decreased == stat:
        return 0.9
    return 1


def calculate_stat(stat_type, base, level, evs, nature):
    if stat_type == 'hp':
        stat = (((2 * base + 31 + (evs / 4)) * level) / 100) + level + 10
    else:
        stat = ((((2 * base + 31 + (evs / 4)) * level) / 100) + 5) * nature
    
    return math.floor(stat)