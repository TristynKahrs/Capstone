from os import system
from functools import reduce
from abc import ABC
from bot.config import Configuration
from queue import Queue
from termcolor import colored
from time import gmtime, strftime

import math, time, ccxt, schedule
import pandas as pd, numpy as np, talib.abstract as ta, mplfinance as mpf, matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

timeframes = {
    '1m' : 60,
    '5m' : 300,
    '15m': 900,
    '1h' : 3600,
    '1d' : 86400,
    '1w' : 604800,
    '1M' : 2592000,
}

class IStrategy(ABC):
    def __init__(self, ticker, config: Configuration):
        self.ticker = ticker
        self.config = config
        
        # if config is passed in, use that, else use default, **kwargs
        if type(config) is Configuration:
            self.config = config.config
            
        for key in ['exchange', 'algorithm', 'plot']:
            if key in self.config:
                if type(self.config[key] is dict):
                    for subkey in self.config[key]:
                        self.__setattr__(subkey, self.config[key][subkey])
                else:
                    self.__setattr__(key, self.config[key])
            else:
                # NOTE: set the attr here with a default value
                raise KeyError(f'{key} must be specified')
            
        self.open_pos = Queue(self.max_open_positions)
        
        exchange_class = getattr(ccxt, self.exchange_name)
        self.exchange = exchange_class({
            'apiKey': self.apiKey,
            'secret': self.secret, 
            'timeout': 30000,
            'enableRateLimit': True,
            'options': { 'adjustForTimeDifference': True }
            })
        self.exchange.set_sandbox_mode(True)
    
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
    
    def update_df(self):
        bars = self.exchange.fetch_ohlcv(self.ticker, timeframe=self.timeframe, limit=self.limit)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        self.df = df
        return self.df
    
    def display(self, df):
        if self.show:
            print(colored('table updated: ' + str(df['timestamp'].iloc[-1]), 'blue'))
            df.timestamp = pd.to_datetime(df.timestamp)
            df.set_index('timestamp', inplace=True)
            fig, axes = mpf.plot(df, figratio=(12, 8), type='candle',
                    style='yahoo', volume=True, mav=(5,10,20),
                    title=self.ticker, ylabel='Price',
                    ylabel_lower='Volume', tight_layout=True,
                    returnfig=True)
            mpf.show(block=False)
            plt.pause(timeframes[self.timeframe] - 1)
            plt.close()
        else:
            system('cls')
            print(colored('table updated: ' + str(df['timestamp'].iloc[-1]), 'blue'))
            color = []
            df = df.tail(self.bars)
            start_index, end_index = df.index[0], df.index[-1] + 1
            for current in range(start_index, end_index):
                try:
                    previous_close = df['close'][current - 1]
                except (IndexError, KeyError):
                    previous_close = df['close'][current]
                current_close = df['close'][current]
                if current_close > previous_close:
                    color.append(colored(str(current_close), 'green'))
                elif current_close < previous_close:
                    color.append(colored(str(current_close), 'red'))
                else:
                    color.append(colored(str(current_close), 'white'))
            df.drop(columns=['close'], inplace=True)
            df['close'] = color
            print(df)
            print(colored('Open Positions: ' + str(self.open_pos.qsize()), 'grey'))
    
    def enter_pos(self):
        print('\033[1m' + colored('entering position', 'green') + '\033[0m')
        
        balance_usdt = float(self.exchange.fetch_balance()['free']['USDT'])
        ticker_price = self.exchange.fetch_ticker(self.ticker)['bid']
        stake_amount = (balance_usdt * self.risk) / ticker_price
        print('balance_usdt: ' + str(balance_usdt), 'ticker_price: ' + str(ticker_price), 'stake_amount: ' + str(stake_amount))
        
        order = self.exchange.create_market_buy_order(self.ticker, stake_amount, {'trading_agreement':'agree'})
        print(colored('bought ' + str(order['amount']) + ' ' + self.ticker + ' at ' + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())), 'green'))
        print(colored(order, 'green'))
        self.open_pos.put(order) # append new position to open_pos, save to db
        # exit()
        return order
    
    def exit_pos(self):
        print('\033[1m' + colored('exiting position', 'red') + '\033[0m')
        order = self.open_pos.get()
        order_amt = order['amount']
        
        symbol = self.ticker[:self.ticker.index('/')]
        symbol_balance = self.exchange.fetch_balance()['free'][symbol]
        isclose = math.isclose(symbol_balance, order_amt, rel_tol=1e-4)
        
        if(order_amt > symbol_balance):
            if isclose:
                order_amt = symbol_balance
            else:
                print('order amount was over the available balance, you should restart the bot and check your balances') 
                    
        order = self.exchange.create_market_sell_order(self.ticker, order_amt)
        print(colored('sold ' + str(order['amount']) + ' ' + self.ticker + ' at ' + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())),'red'))
        print(colored(order, 'red'))
        return order
        
    def check_buy_sell_signals(self) -> pd.DataFrame:
        self.df = self.update_df()
        
        indicators = self.populate_indicators(self.df.copy())
        entry_trend = self.populate_entry_trend(indicators)
        exit_trend = self.populate_exit_trend(entry_trend)
        self.indicators = exit_trend
        
        last_row = len(self.df.index) - 1
        prev_row = last_row - 1
        
        amt_open_pos = self.open_pos.qsize()
        if amt_open_pos < self.max_open_positions:
            if math.isnan(self.indicators['enter_long'][prev_row]) and self.indicators['enter_long'][last_row] == 1:
                self.enter_pos()
        if amt_open_pos > 0:
            if math.isnan(self.indicators['exit_long'][prev_row]) and self.indicators['exit_long'][last_row] == 1:
                self.exit_pos()
        return self.indicators
    
    def run(self):
        try:
            amt_time = 1 if self.show else timeframes[self.timeframe]
            schedule.every(amt_time).seconds.do(self.check_buy_sell_signals) # NOTE: how do i change timeframe?
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            except KeyboardInterrupt:
                self.exit_handler()
        except Exception as e:
            print(e)
            self.exit_handler()
        
    def backtest(self):
        self.update_df()
        # database.backtest_insert(self.config['data'], self.ticker, self.timeframe, self.df) # NOTE: move to backtest here
        # NOTE: analyze indicators and trends, generate report
    
    def exit_handler(self):
        print(colored('Exiting...', 'yellow'))
        for i in range(self.open_pos.qsize()):
            self.exit_pos()
        print(colored('exited gracefully', 'cyan'))
    
if __name__ == '__main__':
    test_config = Configuration('./test_config.json')
    test_algo = IStrategy(ticker = 'ETH/USDT', config = test_config)