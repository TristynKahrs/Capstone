from config import Configuration
import pandas as pd
import schedule
import ccxt
import time
# import talib as ta

# class IStrategy(ABC):
class IStrategy:
    def __init__(self, ticker, config: Configuration):
        self.ticker = ticker
        self.config = config
        
        # if config is passed in, use that
        # if 'config' in kwargs:
        #     self.config = kwargs['config']['algorithm']
        if type(config) is Configuration:
            self.config = config.config
            
        # required parameters
        for key in ['exchange', 'algorithm']:
            if key in self.config:
                # dict keys
                if type(self.config[key] is dict):
                    for subkey in self.config[key]:
                        self.__setattr__(self, subkey, self.config[key][subkey])
                # str keys
                else:
                    self.__setattr__(key, self.config[key])
            else:
                # NOTE: set the attr here with a default value
                raise KeyError(f'{key} must be specified')
        
        self.update_df()
        # run backtest?
    
    def populate_indicators(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        # dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['rsi'] = ['1' if x > 70 else '0' for x in dataframe['open']] # ta.RSI(dataframe, timeperiod=14)
        return dataframe
    
    def populate_entry_trend(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe
    
    def populate_exit_trend(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe
    
    def update_df(self):
        exchange = getattr(ccxt, self.name)()
        bars = exchange.fetch_ohlcv(self.ticker, timeframe=self.timeframe, limit=self.limit)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        self.df = df
        
        indicators = self.populate_indicators(self.df)
        entry_trend = self.populate_entry_trend(indicators)
        exit_trend = self.populate_exit_trend(entry_trend)
        
        # send copy or send same object?
        # self.indicators = exit_trend
        # print(self.indicators)
        print(self.df)
    
    def enter(self): # NOTE: enter a position
        raise NotImplementedError("Should implement enter()!")
    
    def exit(self): # NOTE: exit a position
        raise NotImplementedError("Should implement exit()!")
    
    # @abstractmethod        
    def run(self):
        schedule.every(1).seconds.do(self.update_df) # NOTE: how do i change timeframe?
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.exit_handler()
        
    def backtest(self):
        self.update_df()
        # NOTE: analyze indicators and trends, generate report
    
    def exit_gracefully(self):
        # NOTE: exit all positions and close all connections
        print('exited gracefully')
    
    def exit_handler(self):
        print("Exiting...")
        self.exit_gracefully()
    
if __name__ == '__main__':
    test_config = Configuration('./user_data/config.json').config
    test_algo = IStrategy(ticker = 'DOGE/USDT', config = test_config)
    test_algo.run()