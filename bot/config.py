import json
import os

class Configuration:
    def __init__(self, config_file: str = './data/config.json'): # TODO make config save login TODO handle NoneType error
        create_default_config()
        self.config_file = config_file
        self._base_config = {"startup": {"login":{"username": "", "password": ""}, "config": self.config_file}}
        
        if __exists__(config_file):
            print("Using existing configuration: " + config_file)
            self.config = {}
            self.config = get_config(self.config_file)
            self.assert_login()
        else:
            with open(config_file, 'w') as file:
                self.config = self._base_config
                json.dump(self.config, file, indent=4)
            print("Your configuration could not be found, one has been created for you;\nIt is located at: " + config_file)
    
    def assert_login(self): # TODO verify Login exists
        out = False
        try:
            self.config['startup']
            self.config['startup']['login']
            self.config['startup']['config']
            out = True
        except:
            self.config['startup'] = self._base_config.get('startup')
            self.config['startup']['config'] = self._base_config['startup']['config']
            with open(self.config_file, 'w') as file:
                json.dump(self.config, file, indent=4)
            print('Went into except')
            # print no startup?
            # raise exception
        return out
        
    def set_config(self, config):
        config_file = config['startup']['config']
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
        self.config = config
        return config

    # take a config dict and save it
    # def update_config(self, config_file: str, field): # TODO update
    #     self.config = json.load(config_file)
    #     self.config[field.key] = field.value
        
    def __str__(self):
        return str(self.config)

def __exists__(config_file: str):
    return os.path.isfile(config_file) and os.access(config_file, os.R_OK)

def get_config(config_file: str):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        if(config is None):
            config = {}
        return config
    except:
        print("Could not find configuration file " + config_file)

def create_default_config():
    default_config = {
        "startup": {
            "config": "./data/default_config.json"
        },
        "universe": {
            "symbols": [
                "SPY",
                "DOW",
                "AAPL"
            ]
        },
        "algorithm": {
            "temp_field": 1
        },
        "risk": "risk",
        "entry": "entry?",
        "docker": "docker?"
    }
    with open(default_config['startup']['config'], 'w') as file:
        json.dump(default_config, file, indent=4)
    return default_config

if __name__ == '__main__':
    config_main = Configuration('./data/config_file.json')
    print(config_main)