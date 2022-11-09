from Capstone.bot.config import Configuration as cf

class Universe():
    symbols = []
    
    # TODO: make this work with kwargs
    def __init__(self, config: dict = None):
        if type(config) is cf:
            config = config.config
            
        if config is None:
            config = cf.get_default_config()
            
        if 'filters' in config:
            # TODO: set_symbols() # based off of filters; make a class?
            pass
        elif 'symbols' in config:
            self.symbols = config['symbols']
        # TODO: what if the universe isn't recognized
        # TODO: validate the universe
        
    def get_data(self):
        # TODO: return a list of data frames for the symbols on the timeframe specified
        pass
        
    def __str__(self):
        return str(self.get_symbols())
        
if __name__ == '__main__':
    temp_universe = {'symbols': 'temp universe'}
    main_universe = Universe(temp_universe)