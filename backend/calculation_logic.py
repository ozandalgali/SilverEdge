from __future__ import print_function
import sqlite3
import pandas as pd
import gate_api
from gate_api.exceptions import ApiException, GateApiException

# Get the list of contracts
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)

api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.FuturesApi(api_client)
settle = 'usdt' # str | Settle currency
api_response = api_instance.list_futures_tickers(settle)
source_list = []
for data_point in api_response:
    contract = data_point.contract
    source_list.append(contract)
print(source_list)

# Connect to SQLite database
conn = sqlite3.connect('futures_data.db')
outlier_contracts = []
for contract in source_list:
    print(f"Processing contract: {contract}")
    
    # Query the last 5 records for the specific contract
    print("Running query...")
    df = pd.read_sql_query('''
        SELECT * FROM futures_data
        WHERE contract = ?
        ORDER BY rowid DESC
        LIMIT 10
    ''', conn, params=(contract,))
    print("Query completed.")
    
    # Calculate the VPT
    print("Calculating Average Volume 10...")
    average_volume = df['volume'].mean()
    print(f"Average Volume {average_volume} calculated.")
    df['outlier'] = df['volume'] > average_volume
    df['price_change'] = (df['close_price'] - df['open_price']) / df['open_price'] * 100
    if (df['outlier'].rolling(3).sum() == 3).any():
        outlier_contracts.append(contract)

    df.to_csv('output.csv', mode='a', header=False, index=False)
print(outlier_contracts)
# Close the connection
conn.close()