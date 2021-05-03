from datetime import datetime, timedelta
import pandas as pd
import os

# Create path
pd.set_option('display.max_rows', None)
directory = '/Users/roos/Data/TEST'

# Get trigger logger file
trigger = directory + '/8SBexpB_triggerlogger_2021_Apr_15_1415.csv'
triggers = pd.read_csv(trigger, skiprows=range(1, 20))  # Skip practice trials

# Create dataframe
data_frame = {'trigger': triggers['Trigger'], 'start_time': triggers['TriggerTime']}
data_file = pd.DataFrame(data_frame)
data_file.dropna(inplace=True)

wrong_triggers = data_file.index[(data_file['trigger'] == 9.0) | (data_file['trigger'] == 7.0)]
data_file.drop(wrong_triggers, inplace=True)
data_file.reset_index(drop=True, inplace=True)

# Refactor the trigger times
original_time = datetime(year=1970, month=1, day=1, hour=2)

for time in data_file['start_time']:
    new_time = original_time + timedelta(seconds=time)
    new_time = new_time - timedelta(microseconds=new_time.microsecond)
    data_file['start_time'].replace(time, new_time, inplace=True)

# Add new column with end time of each trial
data_file['end_time'] = ''

# Get locations of triggers 8, 0 and 2
locations = data_file.index[(data_file['trigger'] == 8.0) | (data_file['trigger'] == 0.0)]
locations_2 = data_file.index[(data_file['trigger'] == 2.0)]
data_file['trigger'] = data_file['trigger'].astype(str)

# Make each row one trial
for location in locations:
    data_file.at[location - 2, 'end_time'] = data_file.at[location, 'start_time']
    data_file.at[location - 2, 'trigger'] = str(data_file.at[location - 2, 'trigger']) + '-' + str(
        data_file.at[location, 'trigger'])
    data_file.drop(index=location, inplace=True)

for location in locations_2:
    data_file.drop(index=location, inplace=True)

# Reset index of dataframe
data_file.reset_index(drop=True, inplace=True)

# Get correct responses from BSRT
result = directory + '/8SBexpB_BSRT_staircase_vbeam_2021_Apr_15_1416.csv'
results = pd.read_csv(result, skiprows=range(1, 7))

data_file['response'] = results['response.corr']

data_file.dropna(inplace=True)

# Import iButton data
ibutton_folder = directory + '/' + "8SBexpB"
ibuttons_list = os.listdir(ibutton_folder)

for ibutton in ibuttons_list:
    path = ibutton_folder + '/' + ibutton
    temp = pd.read_csv(path, skiprows=18)
    ibutton_name, rest = ibutton.split('_')
    data_file[ibutton_name] = ''
    print(f"Processing data from {ibutton_name}")

    for time in temp['Date/Time']:
        good_time = pd.to_datetime(time)
        location_temp, = temp.index[(temp['Date/Time'] == time)]
        for trigger_time in data_file['start_time']:
            if good_time == trigger_time:
                location = data_file.index[(data_file['start_time'] == trigger_time)]
                data_file.at[location, ibutton_name] = temp.iloc[location_temp]['Value']
            elif good_time == trigger_time + timedelta(seconds=1):
                location = data_file.index[(data_file['start_time'] == trigger_time)]
                data_file.at[location, ibutton_name] = temp.iloc[location_temp]['Value']


print(data_file)
