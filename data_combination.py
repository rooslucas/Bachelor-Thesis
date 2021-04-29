from datetime import datetime, timedelta
import pandas as pd

directory = '/Users/roos/Data/TEST'
trigger = directory + '/8SBexpA_triggerlogger_2021_Apr_15_1019.csv'
triggers = pd.read_csv(trigger, skiprows=[i for i in range(1, 20)])
data_frame = {'trigger': triggers['Trigger'], 'trigger_time': triggers['TriggerTime']}
data_file = pd.DataFrame(data_frame)
print(data_file)
data_file.drop(index=data_file.index[-1], inplace=True)

original_time = datetime(year=1970, month=11, day=23, hour=2)

for time in data_file['trigger_time']:
    new_time = original_time + timedelta(seconds=time)
    data_file['trigger_time'].replace(time, new_time, inplace=True)

print(data_file)
