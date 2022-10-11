from bot.sparkplug import ignite
from bot.config import get_config, create_default_config, Configuration
from os import system

import os, fnmatch

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
    invalid = True
    while invalid:
        for i in range(0, len(options)):
            print(str(i + 1) + ")\t", str(options[i]))
        print()
        seperator()
        try:
            reply = int(prompt(prompt_text, fail_text))
            if(isinstance(reply, int) and reply <= len(options)):
                invalid = False
            else:
                print(fail_text)
        except:
            print(fail_text)
            seperator()
            print()
        
    return int(reply)

def help():
    clearScreen()
    print("""
You may use the following commands:
    help / h        display this help menu
    login / l       alter login information
    quit / q        exit the CLI
    """)
    seperator()
    
def login(configuration):    
    logged_out = True
    while logged_out:
        print(configuration)
        print('Please enter your brokerage account information:')
        
        username = prompt('\tEnter username: ', '\t[Username is required]\n')
        password = prompt('\tEnter password: ', '\t[Password is required]\n')
                
        login = {'username': username, 'password': password}
        
        # TODO save login in configuration
        config_file = configuration.config['startup']['config']
        
        config_update = get_config(config_file)
        config_update['startup']['login'] = login
        configuration.set_config(config_update)
        
        logged_out = False
    clearScreen()
    
def configs(): # TODO make new configs
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
        first_config = Configuration()
        found_configs.append(first_config.config['startup']['config'])
        
    selected_config = prompt_number("Please select a config file: ", found_configs, 'Please choose a number')

    config = Configuration(found_configs[selected_config - 1])
    
    seperator()
    # clearScreen()
    
    return config

def main():
    system('echo off')
    clearScreen()
    configuration = configs()

    if not configuration.assert_login():
        login(configuration)

    looping = True
    while looping:
        value = prompt('>>> ', 'Please enter a command')
        lower = value.lower()
        
        if lower == 'help' or lower == 'h':
            help()
            
        elif lower == 'config' or lower == 'c':
            configuration = configs()
            
        elif lower == 'login' or lower == 'l':
            login(configuration)
                    
        elif lower == 'quit' or lower == 'q':
            looping = False
            
        elif lower == 'run' or lower == 'r':
            # try:
            ignite(configuration.config_file)
            # except Exception:
            #     print("please login first")
                
        else:
            print('Please enter a valid command; Use "help" or "h" for help')

    clearScreen()
    print('\nExiting\n')
    seperator()
    exit()
    
if __name__ == '__main__':
    main()