from application import Application


if __name__ == "__main__":
    window = Application()
    window.mainloop()
    '''
        for i in range(len(spreads['evs'])):
            for j, stat in enumerate(stats):
                print(stats[j]['stat']['name'])
                print(pkm_stats.calculate_stat(stat['stat']['name'], stat['base_stat'], 50, int(split_evs(spreads['evs'][i])[j]), nature_calc(spreads['nature'][i].lower(), stat['stat']['name'])))
    '''