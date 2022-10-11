from config import Configuration, get_config
from universe import Universe

def ignite(config_file = './data/config.json'):
    default_config = get_config('./data/default_config.json')
    config_file = config_file.replace(' ', '_')
    
    configuration = Configuration(config_file)
    config = configuration.config
    
    #TODO: make sure all fields are dicts
    universe_config = config['universe'] if 'universe' in config else default_config.get('universe')    
    algorithm_config = config['algorithm'] if 'algorithm' in config else default_config.get('algorithm')
    risk_config = config['risk'] if 'risk' in config else default_config.get('risk')
    
    universe = Universe(universe_config)
    if 'symbols' in universe_config:
        universe = Universe(universe_config)
    elif 'filters' in universe_config:
        pass # TODO: implement a universe class here
    
    universe.set_symbols(universe_config['symbols'])
    print('In Sparkplug:', universe.get_symbols())
    
    #enter trades
        #display data
        #save data
        #generate reports
            #json->html->pdf
        #email reports

if __name__ == '__main__':
    ignite()