import pybit
import sqlite3
import json
from pybit.unified_trading import HTTP

session = HTTP()



# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('bybit_futures_data.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS futures_data (
        contract TEXT,
        volume REAL,
        open_price REAL,
        high_price REAL,
        low_price REAL,
        close_price REAL
    )
''')

# Get tickers class

class TickerGetter:
    def __init__(self, session):
        self.session = session

    def get_tickers(self):
        tickerdata = self.session.get_tickers(category="linear")
        symbols = [item['symbol'] for item in tickerdata['result']['list']]
        return symbols
    
    def get_kline(self, category, symbol, interval, limit):
        return self.session.get_kline(category=category, symbol=symbol, interval=interval, limit=limit)

    def filter_OHLCandVolume(self, symbol, kline_data):
        OHLCandVolume = []
        for item in kline_data['result']['list']:
            OHLCandVolume.append([symbol] + [item[i] for i in [1, 2, 3, 4, 6]])
        return OHLCandVolume
    
    def push_to_database(self, filtered_data):
        try:
            data_points = filtered_data[0]
            contract = data_points[0]
            open_price = data_points[1]
            high_price = data_points[2]
            low_price = data_points[3]
            close_price = data_points[4]
            volume = data_points[5]
            c.executemany('''
            INSERT INTO futures_data (contract, volume, open_price, high_price, low_price, close_price)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', data_points)
            conn.commit()
        except Exception as e:
            return f"An error occurred: {e}"  


# Create an object of the class
ticker_getter = TickerGetter(session)

# This is where we get all the tickers available
symbols = ticker_getter.get_tickers()

# Use the object to get the kline data
for symbol in symbols:
    # Use the object to get the kline data
    kline_data = ticker_getter.get_kline(category="linear", symbol=symbol, interval=60, limit=1)
    # Filter the kline data and add the symbol name
    filtered_data = ticker_getter.filter_OHLCandVolume(symbol, kline_data)
    pushed = ticker_getter.push_to_database(filtered_data)
    # Print the filtered data
    print(filtered_data)
    #print(preparation1)

conn.close()
print('completed')

