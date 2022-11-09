from functools import reduce
from config import Configuration
import pandas as pd
import schedule
import ccxt
import time
import talib.abstract as ta
import numpy as np
import math

# class IStrategy(ABC):
class IStrategy:
    def __init__(self, ticker, config: Configuration):
        self.open_pos = []
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
                        self.__setattr__(subkey, self.config[key][subkey])
                # str keys
                else:
                    self.__setattr__(key, self.config[key])
            else:
                # NOTE: set the attr here with a default value
                raise KeyError(f'{key} must be specified')
        
        # run backtest?
    
    def populate_indicators(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        return dataframe
    
    def populate_entry_trend(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        conditions = []
        conditions.append(dataframe['rsi'] < 30)
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'] = 1
        return dataframe
    
    def populate_exit_trend(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        conditions = []
        conditions.append(dataframe['rsi'] > 70)
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'exit_long'] = 1
        return dataframe
    
    def update_df(self): # populate indicators and then run entry and exit at the same time?
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
        print(self.df)
        
    def check_buy_sell_signals(self) -> pd.DataFrame:
        dataframe = self.update_df()
        # if dataframe['enter_long'].iloc[-1] is not None and dataframe['exit_long'].iloc[-1] is not None:
        #     if dataframe['enter_long'].iloc[-1] == 1:
        #         if math.isnan(dataframe['enter_long'].iloc[-2]):
        #             if self.open_pos < 5:
        #                 self.open_pos.append(self.enter())
        #     elif dataframe['exit_long'].iloc[-1] == 1 and math.isnan(dataframe['exit_long'].iloc[-2]): # NOTE: should check if in a trade
        #         self.open_pos.remove(self.exit())
        #     else:
        #         pass
        self.enter()
        self.exit()
        return dataframe
    
    def enter(self): # NOTE: enter a position, return the position
        print('\033[92m' + 'entering position' + '\033[0m')
    
    def exit(self): # NOTE: exit a position, return the position
        print('\033[91m' + 'exiting position' + '\033[0m')
    
    def run(self):
        self.open_pos = 0
        schedule.every(1).second.do(self.check_buy_sell_signals) # NOTE: how do i change timeframe?
        
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
    test_config = Configuration('./user_data/config.json')
    test_algo = IStrategy(ticker = 'DOGE/USDT', config = test_config)
    test_algo.run()