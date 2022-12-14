import json
import os

class Configuration: # TODO: check if there is a singular config file
    def __init__(self, config_file: str = './config.json') -> None: # TODO handle NoneType error TODO inherit from dict?
        # self.create_default_config()
        config_file = config_file.replace(' ', '_')
        
        self._base_config = {"exchange": {
            "name": "",
            "key": "",
            "secret": "",
            "password": ""
        }}
        
        if self.__exists__(config_file):
            print("Using existing configuration: " + config_file)
            self.config = self.get_config(config_file)
        else:
            with open(config_file, 'w') as file:
                self.config = self._base_config
                json.dump(self.config, file, indent=4)
            print("Your configuration could not be found, one has been created for you;\nIt is located at: " + config_file)
          
    def set_config(self, config) -> json:
        config_file = config['startup']['config']
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
        self.config = config
        return config
    
    def get_field(self, field: str) -> json:
        return self.config[field]

    # take a config dict and save it
    # def update_config(self, config_file: str, field): # TODO update
    #     self.config = json.load(config_file)
    #     self.config[field.key] = field.value
        
    def __str__(self) -> str:
        return str(self.config)

    @staticmethod
    def __exists__(config_file: str):
        return os.path.isfile(config_file) and os.access(config_file, os.R_OK)

    @staticmethod
    def get_config(config_file: str):
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
            if(config is None):
                config = {}
            return config
        except:
            print("Could not find configuration file " + config_file)

    @staticmethod
    def create_default_config():
        default_config = {
                "exchange": {
                    "name": "",
                    "key": "",
                    "secret": "",
                    "password": ""
                },
                "universe": {
                    "symbols": ["BTCUSD", "DOGEUSD", "ETHUSD"]
                },
                "strategy": "",
                "risk": "",
                "entry": "",
                "docker": ""
            }
        if not Configuration.__exists__('./data/default_config.json'):
            with open('./user_data/default_config.json', 'w') as file:
                json.dump(default_config, file, indent=4)
        return default_config
    
    @staticmethod
    def get_default_config():
        if Configuration.__exists__('./data/default_config.json'):
            with open('./data/default_config.json', 'r') as file:
                return json.load(file)
        else:
            return Configuration.create_default_config()

if __name__ == '__main__':
    config_main = Configuration('./data/sample_config.json')
    config_dict = config_main.config
    
    print(config_dict['exchange'])
    print(config_main)