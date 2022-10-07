from config import startup, get_config

def ignite(config_file = './data/config.json'):
    default_config = get_config('./data/default_config.json')
    config_file = './data/' + config_file.replace(' ', '_') + '.json'
    
    config = startup(config_file)
    
    assert(config.__contains__('startup')), 'No startup within configuration file ' + config_file
    
    login = config.get('startup').get('login')
    if(login is not None and (login.__contains__('username') and login.__contains__('password'))): 
        username = login.get('username')
        password = login.get('password')
        
        # assert((username != '') & (password != '')), 'Login information is required'
        
        
        # if(__exists__(config.get('config'):
        #     pass
        
        #TODO: make sure all fields are dicts
        universe = config.get('universe') if config.__contains__('universe') else default_config.get('universe')    
        algorithm = config.get('algorithm') if config.__contains__('algorithm') else default_config.get('algorithm')
        risk = config.get('risk') if config.__contains__('risk') else default_config.get('risk')
        
        #enter trades
            #display data
            #save data
            #generate reports
                #json->html->pdf
            #email reports
    else:
        raise Exception("Login failed")

if __name__ == '__main__':
    ignite()