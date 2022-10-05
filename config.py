import json
from pathlib import Path
import os
from collections import Counter

def startup(config_file: str):
    if __exists__(config_file):
        print("Using existing configuration")
        config = get_config(config_file)
        apply_default(config_file)
    else:
        with open(config_file, 'w') as file:
            with open('./data/default_config.json', 'r') as default_file:
                default_config = json.load(default_file)
            json.dump(default_config, file, indent=4)
            config = default_config
        print("Your configuration could not be found, one has been creaded for you")
    return config

def __exists__(config_file: str):
    return os.path.isfile(config_file) and os.access(config_file, os.R_OK)

def apply_default(config_file: str):
    with open('./data/default_config.json', 'r') as default_file:
        default_config = json.load(default_file)
    config = get_config(config_file)
    
    for key, value in default_config.items():
        if key not in config:
            config[key] = value
    with open(config_file, 'w') as file:
        json.dump(default_config, file, indent=4)
    return config
        
def get_config(config_file: str):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

if __name__ == '__main__':
    startup('config_file')