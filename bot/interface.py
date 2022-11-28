from os import system
from functools import reduce
from abc import ABC
import math
import time

import ccxt
import schedule
from queue import Queue
from bot.config import Configuration
import pandas as pd
import numpy as np
import talib.abstract as ta
from termcolor import colored
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mplfinance as mpf

# import database

class IStrategy(ABC):
    def __init__(self, ticker, config: Configuration):
        self.ticker = ticker
        self.config = config
        
        # if config is passed in, use that
        # if 'config' in kwargs:
        #     self.config = kwargs['config']['algorithm']
        if type(config) is Configuration:
            self.config = config.config
            
        for key in ['exchange', 'algorithm']:
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
    
    def update_df(self):
        bars = self.exchange.fetch_ohlcv(self.ticker, timeframe=self.timeframe, limit=self.limit)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        self.df = df
        return self.df
    
    def display(self, df):
        print(colored('table updated: ' + str(df['timestamp'].iloc[-1]), 'blue'))
        df.timestamp = pd.to_datetime(df.timestamp)
        df.set_index('timestamp', inplace=True)
        
        # def animate(i):
        #     timestamp = df['timestamp']
        #     data = 0 # NOTE: get data from df
        
        #     plt.cla()
            
        #     plt.plot(timestamp, data, label='data', type='candle')
        #     plt.tight_layout()
        
        # ani = FuncAnimation(plt.gcf(), animate, interval=1000)
        # plt.show()
        
        # fig, axes = mpf.plot(df, figratio=(12, 8), type='candle',
        #          style='yahoo', volume=True, mav=(5,10,20),
        #          title=self.ticker, ylabel='Price',
        #          ylabel_lower='Volume', tight_layout=True)
        # mpf.show()
        # for ax in axes:
        #     ax.clear()
        plt.close('all')
        plt.pause(0.001)
        fig, axes = mpf.plot(df, figratio=(12, 8), type='candle',
                 style='yahoo', volume=True, mav=(5,10,20),
                 title=self.ticker, ylabel='Price',
                 ylabel_lower='Volume', tight_layout=True)
        mpf.show()
        # fig.cla()
        
        
        # fig, axes = mpf.plot(df, type='candle', mav=mav_tuple, returnfig=True)
        # # Configure chart legend and title
        # axes[0].legend(mav_titles)
        # axes[0].set_title(self.ticker)
        
        
        # system('cls')
        # color = []
        # start_index, end_index = df.index[0], df.index[-1] + 1
        # #print(start_index, end_index)
        # for current in range(start_index, end_index):
        #     #print(current)
        #     try:
        #         previous_close = df['close'][current - 1]
        #     except (IndexError, KeyError):
        #         previous_close = df['close'][current]
        #     current_close = df['close'][current]
        #     if current_close > previous_close:
        #         color.append(colored(str(current_close), 'green'))
        #     elif current_close < previous_close:
        #         color.append(colored(str(current_close), 'red'))
        #     else:
        #         color.append(colored(str(current_close), 'white'))
        # df.drop(columns=['close'], inplace=True)
        # df['close'] = color
        # print(df)
        # print(colored('Open Positions: ' + str(self.open_pos.qsize()), 'grey'))
    
    def enter_pos(self):
        print('\033[1m' + colored('entering position', 'green') + '\033[0m')
        
        balance_usdt = float(self.exchange.fetch_balance()['free']['USDT'])
        ticker_price = self.exchange.fetch_ticker(self.ticker)['bid']
        stake_amount = (balance_usdt * self.risk) / ticker_price
        print('balance_usdt: ' + str(balance_usdt), 'ticker_price: ' + str(ticker_price), 'stake_amount: ' + str(stake_amount))
        
        order = self.exchange.create_market_buy_order(self.ticker, stake_amount, {'trading_agreement':'agree'})
        print(colored('bought ' + str(order['amount']) + ' ' + self.ticker + ' at ' + str(order['price']), 'green'))
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
        
        # print('symbol: ', symbol, ', symbol_balance: ', symbol_balance, ', order_amt: ', order_amt, ', is_close: ', isclose)
        
        if(order_amt > symbol_balance):
            if isclose:
                order_amt = symbol_balance
            else:
                print('order amount was over the available balance, you should restart the bot and check your balances') 
                    
        order = self.exchange.create_market_sell_order(self.ticker, order_amt)
        print(colored('sold ' + str(order['amount']) + ' ' + self.ticker + ' at ' + str(order['price']),'red'))
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
            schedule.every(1).minute.do(self.check_buy_sell_signals) # NOTE: how do i change timeframe?
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
        # NOTE: exit all positions and close all connections
        # self.exchange.close_all_orders(self.ticker)
        print(colored('Exiting...', 'yellow'))
        for i in range(self.open_pos.qsize()):
            self.exit_pos()
        print(colored('exited gracefully', 'cyan'))
    
if __name__ == '__main__':
    test_config = Configuration('./test_config.json')
    test_algo = IStrategy(ticker = 'ETH/USDT', config = test_config)