import requests
import json
import math
from pkm_stats import nature_calc, pokeapi_url


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
        move['name'] = name
        move['damage_class'] = r.json()['damage_class']['name']
        move['power'] = r.json()['power']
        move['stat_changes'] = r.json()['stat_changes']
        move['type'] = r.json()['type']
        return move
    else:
        print("couldn't get move information")


def damage_class(dmg_class):
    return '' if dmg_class == "physical" else 'special-'

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

    attack = damage_class(move['damage_class'])

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


def damage_perc(dmg, hp):
    return str(round(dmg / hp * 100, 1))


def string_calc(attacker, defender, move, min, max):
    attack = damage_class(move['damage_class'])
    new_string = str(attacker['evs'][stat_to_index(attack + "attack")].get())

    if (nature_calc(attacker['nature'].get(), attack + "attack")) == 1.1:
        new_string += "+ "
    elif (nature_calc(attacker['nature'].get(), attack + "attack")) == 0.9:
        new_string += "- "

    new_string += "Atk " if attack == '' else "SpA "

    new_string += attacker['name'].get().capitalize() + " "
    new_string += move['name'].capitalize() + " "

    new_string += "vs. "

    new_string += defender['evs'][stat_to_index('hp')] + " HP / "
    new_string += defender['evs'][stat_to_index(attack + "defense")] + " "

    new_string += "Def " if attack == '' else "SpD "
    new_string += defender['name'].capitalize()

    new_string += ": " + str(min) + "-" + str(max) + " (" + damage_perc(min, defender['new_stats']['hp']) + " - " + damage_perc(max, defender['new_stats']['hp']) + "%)"
    return new_string


def stat_to_index(stat):
        options = { 'hp': 0,
                    'attack': 1,
                    'defense': 2,
                    'special-attack': 3,
                    'special-defense': 4,
                    'speed': 5}
        return options[stat]