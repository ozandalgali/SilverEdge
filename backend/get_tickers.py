from __future__ import print_function
import gate_api
from gate_api.exceptions import ApiException, GateApiException
import json
import sqlite3
import time





# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('futures_data.db')
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





# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.


configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)


api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.FuturesApi(api_client)
settle = 'usdt' # str | Settle currency
api_response = api_instance.list_futures_tickers(settle)
_from = 1546905600 # int | Start time of candlesticks, formatted in Unix timestamp in seconds. Default to`to - 100 * interval` if not specified (optional)
to = 1546935600 # int | End time of candlesticks, formatted in Unix timestamp in seconds. Default to current time (optional)
limit = 10 # int | Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected. (optional) (default to 100)
interval = '3m' # str | Interval time between data points. Note that `1w` means natual week(Mon-Sun), while `7d` means every 7d since unix 0.  Note that 30d means 1 natual month, not 30 days (optional) (default to '5m')
source_list = []
data_points = []  # List to store data points

for data_point in api_response:
    contract = data_point.contract
    source_list.append(contract)  # Addç the contract to the source list
print(len(source_list))
for i in range(10):
    data_points = []  # List to store data points
    for contract in source_list:
        start_time = time.time()  # Start the timer

        api_response = api_instance.list_futures_candlesticks(settle, contract, limit = 1 , interval='3m')
        end_time = time.time()  # End the timer

        try:
            # Get futures candlesticks
            for data_point in api_response:
                volume = data_point.v
                open_price = data_point.o
                high_price = data_point.h
                low_price = data_point.l
                close_price = data_point.c
                data_points.append((contract, volume, open_price, high_price, low_price, close_price))
            # Track the values as desired
            # ...
            # print(contract, volume, open_price, close_price)
  
        except GateApiException as ex:
            print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))

        except ApiException as e:
            print("Exception when calling FuturesApi->list_futures_candlesticks: %s\n" % e)
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken for {contract} run: {elapsed_time} seconds")

    time.sleep(70)    
    c.executemany('''
        INSERT INTO futures_data (contract, volume, open_price, high_price, low_price, close_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data_points)
    conn.commit()
conn.close()
print('completed')