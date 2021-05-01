from datetime import datetime, timedelta
import pandas as pd

# Create path
directory = '/Users/roos/Data/TEST'

# Get trigger logger file
trigger = directory + '/8SBexpA_triggerlogger_2021_Apr_15_1019.csv'
triggers = pd.read_csv(trigger, skiprows=range(1, 20))  # Skip practice trials

# Create dataframe
data_frame = {'trigger': triggers['Trigger'], 'start_time': triggers['TriggerTime']}
data_file = pd.DataFrame(data_frame)
data_file.drop(index=data_file.index[-1], inplace=True)

wrong_triggers = data_file.index[(data_file['trigger'] == 9.0) | (data_file['trigger'] == 7.0)]
data_file.drop(wrong_triggers, inplace=True)
data_file.reset_index(drop=True, inplace=True)

# Refactor the trigger times
original_time = datetime(year=1970, month=1, day=1, hour=2)

for time in data_file['start_time']:
    new_time = original_time + timedelta(seconds=time)
    data_file['start_time'].replace(time, new_time, inplace=True)

# Add new column with end time of each trial
data_file['end_time'] = ''

# Get locations of triggers 8, 0 and 2
locations = data_file.index[(data_file['trigger'] == 8.0) | (data_file['trigger'] == 0.0)]
locations_2 = data_file.index[(data_file['trigger'] == 2.0)]
data_file['trigger'] = data_file['trigger'].astype(str)
print(data_file.info())

# Make each row one trial
for location in locations:
    data_file.at[location - 2, 'end_time'] = data_file.at[location, 'start_time']
    data_file.at[location - 2, 'trigger'] = str(data_file.at[location - 2, 'trigger'] )+ '-' + str(data_file.at[location, 'trigger'])
    data_file.drop(index=location, inplace=True)

for location in locations_2:
    data_file.drop(index=location, inplace=True)

# Reset index of dataframe
data_file.reset_index(drop=True, inplace=True)

# Get correct responses from BSRT
result = directory + '/8SBexpA_BSRT_staircase_vbeam_2021_Apr_15_1019.csv'
results = pd.read_csv(result, skiprows=range(1, 7))
print(results['response.corr'])

data_file['response'] = results['response.corr']

pd.set_option('display.max_rows', None)
print(data_file)
