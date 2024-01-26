from __future__ import print_function
import sqlite3
import pandas as pd
import gate_api
from gate_api.exceptions import ApiException, GateApiException
import csv
import requests


# Send a message to Telegram
def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot6816817424:AAGwlir2UtcyfdvYZTFjrdjsifjmljNo9NQ/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    response = requests.post(url, data=data)
    return response

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

    df['volume_ratio'] = df['volume'] / df['volume'].shift(1)

    df['category'] = df['volume_ratio'].apply(lambda x: 'Big move' if x >= 4 else 'High volume' if x >= 3 else 'Outlier' if x >= 2 else 'normal')

    # Update the outlier condition to include the new categories
    if ((df['outlier'].rolling(3).sum() == 3).any() and 
        (df['open_price'] > df['close_price']).rolling(3).apply(lambda x: all(x)).any() and
        df['category'].isin(['Big move', 'High volume', 'Outlier']).any()):
        outlier_contracts.append(contract)
        print(average_volume)
        
    
    # Send a message to the Telegram bot
        bot_token = "xx"  # Replace with your bot token
        chat_id = "xx"  # Replace with your chat ID
        if df.empty:
            category = 'No data'
        else:
            category = df['category'].iloc[-1]
        message = f"{category} found for contract {contract}"
        send_telegram_message(bot_token, chat_id, message)
    
    df.to_csv('output.csv', mode='a', header=False, index=False)

# Write the outlier contracts to a CSV file
with open('outliers.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Contract'])
    for contract in outlier_contracts:
        writer.writerow([contract])
print("Processing completed.")
print(outlier_contracts)

# Close the connection
conn.close()
