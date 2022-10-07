from distutils import config
from sparkplug import ignite
from config import startup, get_config, set_config, create_default_config
from os import system

import os, fnmatch

# config = get_config('./data/config.json')

system('echo off')
def clearScreen():
    system('cls')
    seperator()
    print('Welcome to the KahrsTech Trading Bot Interactive System')
    seperator()

def seperator():
    print('-' * 55)
    
def prompt(prompt_text: str, fail_text: str):
    invalid = True
    while invalid:
        reply = input(prompt_text)
        if(reply is not None and reply != ''):
            invalid = False
        else:
            print(fail_text)
    return reply

def prompt_number(prompt_text: str, options: list, fail_text: str):
    pass
    invalid = True
    while invalid:
        reply = input(prompt_text)
        if(reply is not None and reply != '' and type(reply) == 'number'):
            invalid = False
        else:
            print(fail_text)
    return reply

def help():
    clearScreen()
    print("""
You may use the following commands:
    help / h        display this help menu
    login / l       alter login information
    quit / q        exit the CLI
    """)
    seperator()
    
def login(config):
    logged_out = True
    while logged_out:
        print('Please enter your brokerage account information:')
        
        username = prompt('\tEnter username: ', '\t[Username is required]\n')
        password = prompt('\tEnter password: ', '\t[Password is required]\n')
                
        login = {'username': username, 'password': password}
        
        # TODO save login in configuration
        config_file = config['startup']['config']
        
        config_update = get_config(config_file)
        config_update['startup']['login'] = login
        set_config(config_update)
        
        logged_out = False
    clearScreen()
    
def configs():
    global config
    
    def find(pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result
    
    print()
    
    found_configs = find('*.json', '.\\')
    try:
        found_configs.remove('.\data\default_config.json')
    except:
        create_default_config()
        
    if(len(found_configs) == 0):
        found_configs.append(startup()['startup']['config'])
    
    for config_file in found_configs:
        print(config_file.strip('./'))
        
    app_config = startup(found_configs[0])
    
    print()
    seperator()
    print('Please select a configuration file:')
    # TODO: MAKE SELECTION
    # clearScreen()
    
    return app_config

def main():
    clearScreen()
    config = configs()

    # TODO CHECK THAT CONFIG HAS VALID LOGIN
    # TODO LOGIN IF NO SET CONFIGURATION HAS NONE
    # TODO SAVE CONFIGURATION

    looping = True
    while looping:
        value = prompt('>>> ', 'Please enter a command')
        lower = value.lower()
        
        if lower == 'help' or lower == 'h':
            help()
            
        elif lower == 'config' or lower == 'c':
            config = configs()
            
        elif lower == 'login' or lower == 'l':
            login(config)
                    
        elif lower == 'quit' or lower == 'q':
            looping = False
            
        elif lower == 'run' or lower == 'r':
            try:
                ignite(config.__getattribute__(config))
            except Exception:
                print("please login first")
                
        else:
            print('Please enter a valid command; Use "help" or "h" for help')

    clearScreen()
    print('\nExiting\n')
    seperator()
    exit()
    
if __name__ == '__main__':
    main()