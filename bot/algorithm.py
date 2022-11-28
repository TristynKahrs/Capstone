import config as cf
import pandas as pd
import ccxt

class Algorithm():
    def __init__(self, **kwargs):
        pass
    
    def backtest(self):
        # NOTE: look at data in the past and generate backtest report based on strategy
        pass
    
    def trade(self):
        # NOTE: run with scheduler on actual live account
        pass
    
    def build_test(self):
        # NOTE: delete later, just for testing
        exchange = ccxt.hitbtc()
        bars = exchange.fetch_ohlcv(self.ticker, timeframe=self.timeframe, limit=self.limit)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        print(df)
        
if __name__ == '__main__':
    
    test_algo = Algorithm(ticker = 'DOGE/USDT', timeframe = '1m', limit = 10)
    test_algo.build_test()
    
    test_config = cf.Configuration('./user_data/config.json').config
    new_test_algo = Algorithm(ticker = 'BTC/USDT', config = test_config)
    new_test_algo.build_test()