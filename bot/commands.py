import sys

default_config = "default_config.json" # TODO: link with default config

def clone():
    print("cloning %s" % args)
    if len(args) > 2:
        if args[2].lower() == '-l' or args[2].lower() == '--location':
            location_arg = args[3].lower() if args[3] else default_config
            print(location_arg)            
            # clone basic user_data project
    else:
        raise AttributeError("Location argument not fufilled")

def backtest():
    print("backtesting %s" % args)
    if len(args) > 3:
        if args[2].lower() == '-c' or args[2].lower() == '--config':
            config_arg = args[3].lower() if args[3] else default_config
            print(config_arg)
            # get config
            # get strategy from config
            # backtest strategy
    else:
        raise AttributeError("Configuration argument not fufilled")

def run():
    print("running %s" % args)
    if len(args) > 3:
        if args[2].lower() == '-c' or args[2].lower() == '--config':
            config_arg = args[3].lower()
            print(config_arg)
            # get config
            # get strategy from config
            # run strategy
    else:
        raise AttributeError("Configuration argument not fufilled")
    
def docker():
    print("dockerizing %s" % args)
    if len(args) > 3:
        if args[2].lower() == '-c' or args[2].lower() == '--config':
            config_arg = args[3].lower() if args[3] else default_config
            print(config_arg)
            # get config
            # dockerize strategy
    else:
        raise AttributeError("Configuration argument not fufilled")

def get_first_arg():
    if len(args) > 1:
        first_arg = args[1].lower()
        
        try:
            if first_arg not in ["get_first_arg"]:
                globals()[first_arg]()
            else:
                raise AttributeError()
        except KeyError:
            print("Please enter a valid command")
        except AttributeError:
            print("ooo you're sneaky; you're trying to break me")
        except Exception as e:
            print("Something went so wrong even we couldn't handle it: %s" % e)
        
    return args

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        print(get_first_arg())
    else:
        pass
        # cli mode?