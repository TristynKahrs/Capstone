import json
from pathlib import Path
import os
from collections import Counter

def startup(config_file: str = './data/config.json'):
    if __exists__(config_file):
        print("Using existing configuration: " + config_file)
        config = get_config(config_file)
    else:
        with open(config_file, 'w') as file:
            config = {"startup": {"login":{"username": "", "password": ""}, "config": config_file}}
            json.dump(config, file, indent=4)
        print("Your configuration could not be found, one has been created for you;\nIt is located at: " + config_file)
    return config

def update_config(config_file: str, field):
    config = json.load(config_file)
    config[field.key] = field.value

def __exists__(config_file: str):
    return os.path.isfile(config_file) and os.access(config_file, os.R_OK)
   
def set_config(config):
    config_file = config['startup']['config']
    with open(config_file, 'w') as file:
        json.dump(config, file, indent=4)
    return config
         
def get_config(config_file: str):
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
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
                "SPY500",
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
    startup('./data/config_file.json')