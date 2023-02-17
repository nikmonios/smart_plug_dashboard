import asyncio
from kasa import SmartPlug
from influxdb import DataFrameClient
import json
import pandas as pd
import time


client = DataFrameClient(host="170.15.0.3", port=8086, database="power_energy", username="admin", password="my strong pwd")

p = SmartPlug("IP of my HS110")

asyncio.run(p.update())

# debug
#print(p.alias)
#print(p.hw_info)
#print(p.emeter_realtime)

# object to string
json_obj = json.dumps(p.emeter_realtime)

# get the unix timestamp as well
timedate = int(time.time())

# string to json
ll = json.loads(json_obj)

# put json values to a list
temp_list = []
temp_list.append(ll['voltage_mv'])
temp_list.append(ll['current_ma'])
temp_list.append(ll['power_mw'])
temp_list.append(ll['total_wh'])

# debug
#print(temp_list)

# make list of column names
col_names = ['volts_mv', 'milliamps', 'power_mw', 'total_wh']

# create empty df with column names
df = pd.DataFrame(columns=col_names)

# add new data to the dataframe
df.loc[len(df)] = temp_list

# set new column timestamp
df['timestamp'] = pd.to_datetime("now") # timedate

# make the timestamp column an index to the df
df.set_index('timestamp', inplace=True)


# debug
print(df)

client.write_points(df, 'smart_plug', protocol='line')

print("done!")
