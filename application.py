import tkinter as tk
from tkinter import IntVar, ttk, font
from damage_calculation import damage_calc, damage_perc, get_move, string_calc
from pkm_stats import *

class Application(tk.Tk):
    def __init__(self):
        
        self.stat_entries = []
        self.stat_label = []

        tk.Tk.__init__(self)
        self.minsize(500, 300)
        self.title("Pokemon")
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(size=12)

        validate_level_wrapper = self.register(self.validate_level)
        validate_evs_wrapper = self.register(self.validate_evs)

        self.pokemon = {"new_stats": {'hp':IntVar(), 'attack':IntVar(), 'defense':IntVar(), 'special-attack':IntVar(), 'special-defense':IntVar(), 'speed':IntVar()}}

        self.main_frame = tk.Frame(self)
        self.main_frame.grid()

        self.pokemon['name'] = tk.StringVar()

        self.pokemon_species = ttk.Combobox(self.main_frame, values=get_all_pokemon(), textvariable=self.pokemon['name'], font=self.defaultFont)
        self.pokemon_species.current(0)
        
        self.pokemon_species.bind('<<ComboboxSelected>>', self.set_base_stats)
        self.pokemon_species.bind('<<ComboboxSelected>>', lambda event: [self.set_final_stats(event, i) for i in range(6)], add='+')
        self.pokemon_species.grid()

        self.level = IntVar(value=50)
        self.level_spinbox = tk.Spinbox(self.main_frame, from_=0.0, to_=100.0, textvariable=self.level, 
                    validatecommand=(validate_level_wrapper, '%P'), validate='key',
                    font=self.defaultFont,width=5)

        self.level_spinbox.bind('<ButtonRelease-1>', lambda event: [self.set_final_stats(event, i) for i in range(6)])
        self.level_spinbox.bind('Key', lambda event: [self.set_final_stats(event, i) for i in range(6)])
        self.level_spinbox.grid()

        self.evs_frame = tk.Frame(self)
        self.evs_frame.grid(column=0)

        self.pokemon['nature'] = tk.StringVar()
        self.nature_combobox = ttk.Combobox(self.main_frame, values=get_all_natures(), textvariable=self.pokemon['nature'], font=self.defaultFont)
        self.nature_combobox.current(0)
        self.nature_combobox.bind('<<ComboboxSelected>>', lambda event: [self.set_final_stats(event, i) for i in range(6)])
        self.nature_combobox.grid()

        self.set_base_stats()

        self.pokemon['evs'] = []
        
        for i in range(6):
            stat = IntVar()
            self.stat_entries.append(tk.Spinbox(self.evs_frame, from_=0.0, to_=252.0, 
                        textvariable=stat, validatecommand=(validate_evs_wrapper, '%P'), validate="key",
                        increment=4, font=self.defaultFont, width=4))
            self.stat_entries[i].bind('<ButtonRelease-1>', lambda event, i=i:self.set_final_stats(event, i))
            self.stat_entries[i].grid(column=0, row=i)
            self.pokemon['evs'].append(stat)

            self.set_final_stats(None, i)

            self.stat_label.append(tk.Label(self.evs_frame, textvariable=self.pokemon['new_stats'][self.index_to_stat(i)]))
            self.stat_label[i].grid(column=1, row=i)

        self.calc_button = tk.Button(self, text="Calculate", command=self.calc_all)
        self.calc_button.grid()
            


    def set_base_stats(self, event=None):
        self.pokemon.update(get_pokemon_stats(self.pokemon['name'].get()))


    def set_final_stats(self, event, i):
        self.pokemon['new_stats'][self.index_to_stat(i)].set(calculate_stat(self.pokemon['stats'][i]['stat']['name'], self.pokemon['stats'][i]['base_stat'], self.level.get(), self.pokemon['evs'][i].get(), nature_calc(self.nature_combobox.get(), self.pokemon['stats'][i]['stat']['name'])))

    def calc_all(self):
        for mon in get_most_used():
            stats = get_pokemon_stats(mon)
            spreads = get_pokemon_spreads(mon)
            for i in range(len(spreads['evs'])):
                evs = split_evs(spreads['evs'][i])
                new_stats = {}
                for j, stat in enumerate(stats['stats']):
                    new_stats[self.index_to_stat(j)] = calculate_stat(stat['stat']['name'], stat['base_stat'], 50, int(evs[j]), nature_calc(spreads['nature'][i].lower(), stat['stat']['name']))
                new_pokemon = { 'name': mon,
                                'evs': evs,
                                'new_stats': new_stats,
                                'type': stats['type']}
                min, max = damage_calc(int(self.level.get()), self.pokemon, new_pokemon, get_move('psyshock'), 1, False, False)
                print(string_calc(self.pokemon, new_pokemon, get_move('psyshock'), min, max), flush=True)


    def index_to_stat(self, i):
        options = { 0: 'hp',
                    1: 'attack',
                    2: 'defense',
                    3: 'special-attack',
                    4: 'special-defense',
                    5: 'speed'}
        return options[i]


    def validate_level(self, level):
        try:
            level = int(level)
            if level > 0 and level <= 100:
                #for i in range(6): self.set_final_stats(None, i)
                return True
        except Exception as e:
            print("level", e, flush=True)
        return False

    
    def validate_evs(self, evs):
        try:
            evs = int(evs)
            if evs > 0 and evs <= 252:
                return True
        except Exception as e:
            print("evs", e, flush=True)
        return False