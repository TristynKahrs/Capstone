import sqlite3
from backtest_data import BacktestData

def create_backtest_table(path, ticker, timeframe):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS backtest_{}_{}(
        ticker TEXT,
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
        )""".format(ticker, timeframe))
    conn.commit()
    conn.close()

def get_backtest_data(path, ticker, timeframe):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('SELECT * FROM backtest_{}_{}'.format(ticker, timeframe))
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

def backtest_insert(path, ticker, timeframe, data):
    create_backtest_table(path, ticker, timeframe)
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("INSERT INTO backtest_{}_{} VALUES (?, ?, ?, ?, ?, ?, ?)".format(ticker, timeframe), tuple(data))
    conn.commit()
    conn.close()

def drop_backtest_table(path, ticker, timeframe):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS backtest_{}_{}".format(ticker, timeframe))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # create_table("./user_data/data/data.db", "BTC", "1m")
    data = get_backtest_data("./user_data/data/data.db", "BTC", "1m")
    print(data)
    drop_backtest_table("./user_data/data/data.db", "BTC", "1m")