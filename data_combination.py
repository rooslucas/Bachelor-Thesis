from datetime import datetime, timedelta
import pandas as pd
import os

# Create path
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
directory = '/Users/roos/Data'

# Create loop for participants by trigger files
trigger_folder = directory + '/TriggerLogger/BSRT'
trigger_list = os.listdir(trigger_folder)
trigger_list.remove('.DS_Store')

for participant in trigger_list:
    participant_id = participant.split('_')
    participant_id = participant_id[0]

    print(f"Processing data from participant {participant_id}")
    trigger_path = trigger_folder + '/' + participant
    triggers = pd.read_csv(trigger_path)  # Skip practice trials

    # Create dataframe
    data_frame = {'trigger': triggers['Trigger'], 'start_time': triggers['TriggerTime']}
    data_file = pd.DataFrame(data_frame)

    # Drop all rows before start trigger
    start, = data_file.index[data_file['trigger'] == 20.0]
    data_file.drop(range(1, start), inplace=True)
    data_file.dropna(inplace=True)

    # Remove wrong triggers
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

    # Drop the other triggers
    for location in locations_2:
        data_file.drop(index=location, inplace=True)

    # Reset index of dataframe
    data_file.reset_index(drop=True, inplace=True)

    # TODO: fill in if no such file exists
    # Get correct responses from BSRT
    results_folder = directory + '/BSRT Performance'
    results_list = os.listdir(results_folder)
    for file in results_list:

        if file.startswith(participant_id):
            results_path = results_folder + '/' + file
            results = pd.read_csv(results_path, skiprows=range(1, 7))
            break
        else:
            results = None
    if results is not None:
        data_file['results'] = results['response.corr']
    else:
        data_file['results'] = ''
        # for trigger in data_file['trigger']:
        #     loc = data_file.index[data_file['trigger'] == trigger]
        #     if trigger == '1.0-8.0':
        #         data_file.at[loc, 'results'] = 1.0
        #     elif trigger == '1.0-0.0':
        #         data_file.at[loc, 'results'] = 0.0
        #
        # missing_results = data_file.index[data_file['results'] == 99]
        # for error in missing_results:
        #     data_file.drop(error, inplace=True)

    data_file.dropna(inplace=True)

    # Import iButton data
    ibutton_folder = directory + '/iButton' + '/' + participant_id
    ibuttons_list = os.listdir(ibutton_folder)

    # Add each ibutton to the dataframe
    for ibutton in ibuttons_list:
        path = ibutton_folder + '/' + ibutton
        temp = pd.read_csv(path, skiprows=18)
        ibutton_name, rest = ibutton.split('_')
        data_file[ibutton_name] = 99.9
        print(f"Processing data from {ibutton_name}")

    # Get temperature from start time of the trial
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

        # Drop missing trials
        missings = data_file.index[data_file[ibutton_name] == 99.9]
        for missing in missings:
            data_file.drop(missing, inplace=True)

    # Calculate three DPGs
    print("Calculate DPG_finger-chest")
    data_file['DPG_finger-chest'] = data_file['4B0000004516B141'] - data_file['9A00000045146841']

    print("Calculate DPG_nose-forehead")
    data_file['DPG_nose-forehead'] = data_file['CB000000452D7441'] - data_file['F9000000452CCF41']

    print("Calculate DPG_pinna-mastoid")
    data_file['DPG_pinna-mastoid'] = data_file['76000000452C9741'] - data_file['7200000045201D41']

    # Safe file to a csv
    data_file.to_csv(r'/Users/roos/Data/Trials/trials' + participant_id + '.csv', index=False, header=True)

    # TODO: Add demographic data

# Combine all trials in one file
# trials_folder = directory + '/Trials'
# trials_list = os.listdir(trials_folder)
# all_trials = glob.glob(os.path.join(trials_folder, '*.csv'))
#
# combined_trials = pd.concat([pd.read_csv(f, delimiter='t', encoding='UTF-16') for f in all_trials])
# combined_trials.to_csv("r'/Users/roos/Data/alltrials.csv")
