import tkinter as tk
from tkinter import StringVar, ttk, font
from damage_calculation import damage_calc, get_move
from pkm_stats import *

class Application(tk.Tk):
    def __init__(self):
        
        self.evs = []
        self.stat_entries = []
        self.stat_label = []

        tk.Tk.__init__(self)
        self.minsize(500, 300)
        self.title("Pokemon")
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(size=12)

        self.pokemon = {"new_stats": {'hp':StringVar(), 'attack':StringVar(), 'defense':StringVar(), 'special-attack':StringVar(), 'special-defense':StringVar(), 'speed':StringVar()}}

        self.main_frame = tk.Frame(self)
        self.main_frame.grid()

        self.pokemon_species = ttk.Combobox(self.main_frame, values=get_all_pokemon(), font=self.defaultFont)
        self.pokemon_species.current(0)
        
        self.pokemon_species.bind('<<ComboboxSelected>>', self.set_base_stats)
        self.pokemon_species.bind('<<ComboboxSelected>>', lambda event: [self.set_final_stats(event, i) for i in range(6)], add='+')
        self.pokemon_species.grid()

        self.level = StringVar(value=50)
        self.level_spinbox = tk.Spinbox(self.main_frame, from_=0.0, to_=100.0, textvariable=self.level, state="readonly", font=self.defaultFont, width=5)
        self.level_spinbox.bind('<ButtonRelease-1>', lambda event: [self.set_final_stats(event, i) for i in range(6)])
        self.level_spinbox.grid()

        self.evs_frame = tk.Frame(self)
        self.evs_frame.grid(column=0)

        self.nature_combobox = ttk.Combobox(self.main_frame, values=get_all_natures(), font=self.defaultFont)
        self.nature_combobox.current(0)
        self.nature_combobox.bind('<<ComboboxSelected>>', lambda event: [self.set_final_stats(event, i) for i in range(6)])
        self.nature_combobox.grid()

        self.set_base_stats()

        for i in range(6):
            stat = tk.StringVar()
            self.stat_entries.append(tk.Spinbox(self.evs_frame, from_=0.0, to_=252.0, textvariable=stat, increment=4, state="readonly", font=self.defaultFont, width=4))
            self.stat_entries[i].bind('<ButtonRelease-1>', lambda event, i=i:self.set_final_stats(event, i))
            self.stat_entries[i].grid(column=0, row=i)
            self.evs.append(stat)

            self.set_final_stats(None, i)

            self.stat_label.append(tk.Label(self.evs_frame, textvariable=self.pokemon['new_stats'][self.index_to_stat(i)]))
            self.stat_label[i].grid(column=1, row=i)

        self.calc_button = tk.Button(self, text="Calculate", command=self.calc_all)
        self.calc_button.grid()
            


    def set_base_stats(self, event=None):
        self.pokemon.update(get_pokemon_stats(self.pokemon_species.get()))


    def set_final_stats(self, event, i):
        self.pokemon['new_stats'][self.index_to_stat(i)].set(calculate_stat(self.pokemon['stats'][i]['stat']['name'], self.pokemon['stats'][i]['base_stat'], int(self.level.get()), int(self.evs[i].get()), nature_calc(self.nature_combobox.get(), self.pokemon['stats'][i]['stat']['name'])))

    def calc_all(self):
        for mon in get_most_used():
            stats = get_pokemon_stats(mon)
            spreads = get_pokemon_spreads(mon)
            for i in range(len(spreads['evs'])):
                new_stats = {}
                for j, stat in enumerate(stats['stats']):
                    new_stats[self.index_to_stat(j)] = calculate_stat(stat['stat']['name'], stat['base_stat'], 50, int(split_evs(spreads['evs'][i])[j]), nature_calc(spreads['nature'][i].lower(), stat['stat']['name']))
                new_pokemon = { 'new_stats': new_stats,
                                'type': stats['type']}
                print(damage_calc(int(self.level.get()), self.pokemon, new_pokemon, get_move('psyshock'), 1, False, False), flush=True)


    def index_to_stat(self, i):
        options = { 0: 'hp',
                    1: 'attack',
                    2: 'defense',
                    3: 'special-attack',
                    4: 'special-defense',
                    5: 'speed'}
        return options[i]