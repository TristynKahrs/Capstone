import json
from pathlib import Path
import os

config_file = 'config.json'
default_config_file = 'default_config.json'


def startup():
    if os.path.isfile(config_file) and os.access(config_file, os.R_OK):
        config = get_config()
    else:
        with open(config_file, 'w') as file:
            with open(default_config_file, 'r') as default_file:
                default_config = json.load(default_file)
            json.dump(default_config, file, indent=4)
            config = default_config
        print("Config created successfully")
    return config
        
def get_config():
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

if __name__ == '__main__':
    startup()