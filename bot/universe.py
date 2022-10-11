from config import get_config
import abc

class Universe(metaclass=abc.ABCMeta):
    def __init__(self, universe_config: dict = None):
        if universe_config is None: # TODO: check for other discrepancies in config
            universe_config = get_config('./data/default_config.json')['universe']
            
        if 'filters' in universe_config:
            # TODO: set_symbols() # based off of filters; make a class?
            pass
        elif 'symbols' in universe_config:
            self.set_symbols(universe_config['symbols']) 
        # TODO: what if the universe isn't recognized
        # TODO: validate the universe
        
    def get_symbols(self):
        return self.symbols
    
    def set_symbols(self, symbols): # implement filters
        self.symbols = symbols
        
    def __str__(self):
        return str(self.get_symbols())
        
if __name__ == '__main__':
    temp_universe = {'symbols': 'temp universe'}
    main_universe = Universe(temp_universe)