from config import Configuration as cf
from universe import Universe
from algorithm import Algorithm

def ignite(config_file = './data/config.json'):
    default_config = cf.create_default_config()
    
    configuration = cf(config_file)
    config = configuration.config
    
    #TODO: make sure all fields are dicts
    universe_config = config['universe'] if 'universe' in config else default_config.get('universe')    
    algorithm_config = config['algorithm'] if 'algorithm' in config else default_config.get('algorithm')
    risk_config = config['risk'] if 'risk' in config else default_config.get('risk')
    
    universe = Universe(universe_config).symbols
    print(universe)
    
    algorithm = Algorithm(universe, algorithm_config)
    print(algorithm)
    
    #enter trades
        #display data
        #save data
        #generate reports
            #json->html->pdf
        #email reports

if __name__ == '__main__':
    ignite()