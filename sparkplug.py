from config import startup, apply_default

def main():
    #run cli
    
    config = startup('./data/config.json')
    
    login = config.get('startup').get('login')
    if (login.get('username') == '') | (login.get('password') == ''):
        print('Login information is required, please enter your brokerage account to try again.')
        exit()
    else:
        #TODO check login info is valid
        pass
    
    print(config)
    
    apply_default('./data/config.json')
    #run universe selection
    universe = config.get('universe')
    
    #run algoritm selection
    algorithm = config.get('algoritm')
    
    #calculate risk
    risk = config.get('risk')
    
    #enter trades
        #display data
        #save data
        #generate reports
            #json->html->pdf
        #email reports

if __name__ == '__main__':
    main()