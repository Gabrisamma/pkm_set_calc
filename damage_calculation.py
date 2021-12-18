import requests
import json
import math
from pkm_stats import pokeapi_url


def get_all_moves():
    r = requests.get(pokeapi_url + 'move')
    if r.status_code:
        moves = []
        for move in r.json()['results']: moves.append(move['name'])
        return moves
    else:
        print("couldn't get moves")


def get_move(name):
    r = requests.get(pokeapi_url + 'move/' + name)
    if r.status_code:
        move = dict()
        move['damage_class'] = r.json()['damage_class']['name']
        move['power'] = r.json()['power']
        move['stat_changes'] = r.json()['stat_changes']
        move['type'] = r.json()['type']
        return move
    else:
        print("couldn't get move information")


def damage_split_targets(targets):
    return 1 if targets == 1 else 0.75


def is_STAB(move_type, pokemon_type):
    return 1.5 if pokemon_type == move_type else 1


def is_critical(critical):
    return 1.5 if critical else 1


def is_burned(burn):
    return 0.5 if burn else 1


def damage_calc(level, attacker, defender, move, targets, critical, burn):
    
    if move['power'] == 0:
        return 0, 0

    attack = '' if move['damage_class'] else 'special-'

    max_damage = ((2 * level / 5) * move['power'] * float(attacker['new_stats'][attack + 'attack'].get()) / defender['new_stats'][attack + 'defense'] / 50 + 2)
    max_damage *= damage_split_targets(targets) * is_critical(critical) * is_STAB(move['type'], attacker['type']) * type_effectiveness(move['type'], defender['type']) * is_burned(burn)

    min_damage = max_damage * 0.85

    return math.floor(min_damage), math.floor(max_damage)


def type_effectiveness(move_type, pokemon_types):
    f = open('type-chart.json')
    type_chart = json.load(f)

    damage = 1
    for pokemon_type in pokemon_types:
        damage *= type_chart[move_type['name']][pokemon_type['type']['name']]
    f.close()
    return damage
