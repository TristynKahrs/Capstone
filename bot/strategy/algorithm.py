from config import Configuration as cf
import pandas as pd
import ccxt

class Algorithm():
    def __init__(self, ticker, **config):
        self.ticker = ticker
        
        # reset config if it is passed as a config dictionary
        if type(config) is cf:
            config = config.config
        elif 'config' in config:
            # NOTE: make work with Configuration items
            # if type(config['config']) is cf:
            #     config = config.config
            temp_config = config['config']
            if 'algorithm' in temp_config:
                config = config['config']['algorithm']
            
        # set attributes based on configuration
        for key in ['timeframe', 'limit']:
            if key in config:
                self.__setattr__(key, config[key])
                # print(self.__getattribute__(key))
            else:
                raise KeyError(f'{key} must be specified')
    
    def backtest(self):
        # NOTE: look at data in the past and generate backtest report based on strategy
        pass
    
    def trade(self):
        # NOTE: run with scheduler on actual live account
        pass
    
    def build_test(self):
        # NOTE: delete later, just for testing
        exchange = ccxt.kraken()
        bars = exchange.fetch_ohlcv(self.ticker, timeframe=self.timeframe, limit=self.limit)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        print(df)
        
if __name__ == '__main__':
    test_algo = Algorithm(ticker = 'DOGE/USDT', timeframe = '1m', limit = 10)
    test_algo.build_test()
    
    test_config = cf('./data/config.json').config
    new_test_algo = Algorithm(ticker = 'BTC/USDT', config = test_config)
    new_test_algo.build_test()