# Written by Rosalie Lucas
# Last update 21/05/2021

from datetime import datetime, timedelta
import time
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

# Loop through all the participants
for participant in trigger_list[1:2]:
    # Safe the participant id
    participant_id = participant.split('_')
    participant_id = participant_id[0]

    print(f"Processing data from participant {participant_id}")
    trigger_path = trigger_folder + '/' + participant
    triggers = pd.read_csv(trigger_path)

    # Create dataframe
    data_frame = {'trigger': triggers['Trigger'], 'start_time': triggers['TriggerTime']}
    data_file = pd.DataFrame(data_frame)

    # Drop all rows before start trigger --> drop practice trials
    start, = data_file.index[data_file['trigger'] == 20.0]
    data_file.drop(range(1, start), inplace=True)
    data_file.dropna(inplace=True)

    # Refactor the trigger times
    original_time = datetime(year=1970, month=1, day=1, hour=2)

    for time in data_file['start_time']:
        new_time = original_time + timedelta(seconds=time)
        # new_time = new_time - timedelta(microseconds=new_time.microsecond)
        data_file['start_time'].replace(time, new_time, inplace=True)

    # Add new column with end time of each trial
    data_file['end_time'] = ''

    # Get locations of triggers 8, 0 and 1
    locations = data_file.index[(data_file['trigger'] == 8.0) | (data_file['trigger'] == 0.0)]
    locations_2 = data_file.index[(data_file['trigger'] == 1.0)]
    data_file['trigger'] = data_file['trigger'].astype(str)

    # Make each row one trial from target to response
    for location in locations:
        data_file.at[location - 1, 'end_time'] = data_file.at[location, 'start_time']
        data_file.at[location - 1, 'trigger'] = str(data_file.at[location - 1, 'trigger']) + '-' + str(
            data_file.at[location, 'trigger'])
        data_file.drop(index=location, inplace=True)

    # Drop the other triggers
    for location in locations_2:
        data_file.drop(index=location, inplace=True)

    # Reset index of dataframe
    data_file.reset_index(drop=True, inplace=True)

    # TODO: Get alertness and sleepiness from results
    # Get correct responses from BSRT
    # results_folder = directory + '/BSRT Performance'
    # results_list = os.listdir(results_folder)
    # for file in results_list:
    #
    #     if file.startswith(participant_id):
    #         results = None
    #         # results_path = results_folder + '/' + file
    #         # results = pd.read_csv(results_path, skiprows=range(1, 7))
    #         break
    #     else:
    #         results = None
    # if results is not None:
    #     data_file['results'] = results['response.corr']
    # else:

    # Get responses from triggers
    data_file['results'] = ''
    for trigger in data_file['trigger']:
        loc = data_file.index[data_file['trigger'] == trigger]
        if trigger == '2.0-8.0':
            data_file.at[loc, 'results'] = 1.0
        elif trigger == '2.0-0.0':
            data_file.at[loc, 'results'] = 0.0
        else:
            data_file.at[loc, 'results'] = 99

        missing_results = data_file.index[data_file['results'] == 99]
        for error in missing_results:
            data_file.drop(error, inplace=True)

    data_file.dropna(inplace=True)

    # TODO: add FLIR data
    print("Processing FLIR data")
    flir_folder = directory + '/FLIR'
    flir_list = os.listdir(flir_folder)
    for file in flir_list:
        if file.startswith(participant_id):
            flir_path = flir_folder + '/' + file
            flir_data = pd.read_excel(flir_path, skiprows=range(0, 12))
            flir_data['good_time'] = ''
            data_file['El1.Average'] = 99.9
            data_file['El2.Average'] = 99.9

    for point in range(len(flir_data['Time'])):
        ttime = str(flir_data.at[point, 'Time'])
        good_time = pd.to_datetime(ttime) + timedelta(milliseconds=int(flir_data.at[point, 'Milliseconds']))
        good_time = datetime.combine(pd.to_datetime(flir_data.at[point, 'Date']), good_time.time())
        flir_data.at[point, 'good_time'] = good_time

    for time in data_file['start_time']:
        row, = data_file.index[(data_file['start_time'] == time)]
        difference = datetime.now() - time
        print(time)

        for ttime in flir_data['good_time']:
            if int((time - datetime(1970,1,1)).total_seconds()) == int((ttime - datetime(1970,1,1)).total_seconds()):
                diff = time - ttime
                if diff < difference:
                    difference = diff
                    nearest_time = ttime
            elif int((time - datetime(1970,1,1)).total_seconds()) + 1 == int((ttime - datetime(1970,1,1)).total_seconds()):
                break
        #nearest_value = min(data_file['start_time'], key=lambda date: abs((good_time-date).microseconds()))
        print(nearest_time)
        print('Add values to this point')
        data_file.at[row, 'El1.Average'] = flir_data.iloc[point]['El1.Average']
        data_file.at[row, 'El2.Average'] = flir_data.iloc[point]['El2.Average']

    print(data_file)
    # TODO: change times.
    for time in data_file['start_time']:
        new_time = time - timedelta(microseconds=time.microsecond)
        data_file['start_time'].replace(time, new_time, inplace=True)

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

        # Get temperature from 4 seconds before target presenting (shortest interval)
        for time in temp['Date/Time']:
            good_time = pd.to_time(time)
            location_temp, = temp.index[(temp['Date/Time'] == time)]
            for trigger_time in data_file['start_time']:
                if good_time == trigger_time - timedelta(seconds=4):
                    location = data_file.index[(data_file['start_time'] == trigger_time)]
                    data_file.at[location, ibutton_name] = temp.iloc[location_temp]['Value']
                elif good_time == trigger_time - timedelta(seconds=5):  # not available do 5 seconds before
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

    # # TODO: Add demographic data
    # print("Adding data from the questionnaires")
    # questionnaire_folder = directory + '/Questionnaires/questionnaire_data.csv'
    # questionnaire_file = pd.read_csv(questionnaire_folder)
    # row_number, = questionnaire_file.index[(questionnaire_file['PPID'] == participant_id)]
    # data_file['Gender'] = questionnaire_file.at[row_number, 'Gender']
    # data_file['type'] = questionnaire_file.at[row_number, 'type']
    # # # data_file['PSQI'] = questionnaire_file.at[row_number, 'total_score_PSQI']

    # Safe file to a csv
    data_file.to_csv(r'/Users/roos/Data/Trials/trials' + participant_id + '.csv', index=False, header=True)
