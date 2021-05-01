from datetime import datetime, timedelta
import pandas as pd

directory = '/Users/roos/Data/TEST'
trigger = directory + '/8SBexpA_triggerlogger_2021_Apr_15_1019.csv'
triggers = pd.read_csv(trigger, skiprows=range(1, 20))
data_frame = {'trigger': triggers['Trigger'], 'start_time': triggers['TriggerTime']}
data_file = pd.DataFrame(data_frame)
data_file.drop(index=data_file.index[-1], inplace=True)

original_time = datetime(year=1970, month=1, day=1, hour=2)

for time in data_file['start_time']:
    new_time = original_time + timedelta(seconds=time)
    data_file['start_time'].replace(time, new_time, inplace=True)

data_file['end_time'] = ''
locations = data_file.index[(data_file['trigger'] == 8.0) | (data_file['trigger'] == 0.0)]
for location in locations:
    data_file.at[location - 2, 'end_time'] = data_file.at[location, 'start_time']

print(data_file)
