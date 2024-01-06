from __future__ import print_function
import gate_api
from gate_api.exceptions import ApiException, GateApiException
import json
# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)

api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.FuturesApi(api_client)
settle = 'usdt' # str | Settle currency
api_response2 = api_instance.list_futures_tickers(settle)
_from = 1546905600 # int | Start time of candlesticks, formatted in Unix timestamp in seconds. Default to`to - 100 * interval` if not specified (optional)
to = 1546935600 # int | End time of candlesticks, formatted in Unix timestamp in seconds. Default to current time (optional)
limit = 50 # int | Maximum recent data points to return. `limit` is conflicted with `from` and `to`. If either `from` or `to` is specified, request will be rejected. (optional) (default to 100)
interval = '5m' # str | Interval time between data points. Note that `1w` means natual week(Mon-Sun), while `7d` means every 7d since unix 0.  Note that 30d means 1 natual month, not 30 days (optional) (default to '5m')

vol = api_response2[0].contract
print(vol)

# for data_point2 in api_response2:
#     contract = data_point2.contract
#     api_response = api_instance.list_futures_candlesticks(settle, contract, interval='5m')

#     try:
#         # Get futures candlesticks

#     ##print(api_response)

#     # Track 'v', 'o', and 'c' values
#         for data_point in api_response:
#             volume = data_point.v
#             open_price = data_point.o
#             close_price = data_point.c
        
#         # Track the values as desired
#         # ...
#         print(contract,volume, open_price, close_price)
  
    # except GateApiException as ex:
    #     print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))

    # except ApiException as e:
    #     print("Exception when calling FuturesApi->list_futures_candlesticks: %s\n" % e)
