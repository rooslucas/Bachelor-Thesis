# Written by Rosalie Lucas
# Last update 05/06/2021
# Useful for combining Triggerlogger, iButton, FLIR and questionnaire data
# For the BSRT

# Data structure in the following folders
# [Data] --------- [FLIR] |
#                  [Questionnaires] |
#                  [TriggerLogger] --------- [BSRT]
#                  [iButton] --------------- [Participant folder]

# Import necessary libraries
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
i = 1
# Loop through all the participants
for participant in trigger_list:
    print(f"\n Participant {i}/{len(trigger_list)}")
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
    data_file.reset_index(drop=True, inplace=True)

    # Add the flir data
    print("Processing FLIR data")
    flir_folder = directory + '/FLIR'
    flir_list = os.listdir(flir_folder)

    # Import the files
    for file in flir_list:
        if file.startswith(participant_id):
            # FLIR = True
            flir_path = flir_folder + '/' + file
            flir_data = pd.read_excel(flir_path, skiprows=range(0, 12))
            # Create the right columns
            flir_data['good_time'] = ''
            data_file['FLIR_forehead'] = 99.9
            data_file['FLIR_nose'] = 99.9
            break
        else:
            # FLIR = False
            flir_data = None

    if flir_data is not None:
        # Reset times of flir data
        for point in range(len(flir_data['Time'])):
            ttime = str(flir_data.at[point, 'Time'])
            good_time = pd.to_datetime(ttime) + timedelta(milliseconds=int(flir_data.at[point, 'Milliseconds']))
            good_time = datetime.combine(pd.to_datetime(flir_data.at[point, 'Date']), good_time.time())
            flir_data.at[point, 'good_time'] = good_time

        # Track trials and start time in file
        trial = 0
        start = 0
        # Loop through trials
        for time in data_file['start_time']:
            matches_el1 = []
            matches_el2 = []
            row, = data_file.index[(data_file['start_time'] == time)]
            difference = datetime.now() - time

            # Add values from nearest time sample
            for time_f in range(start, len(flir_data['good_time'])):
                ttime = flir_data.iloc[time_f]['good_time']
                if int((time - datetime(1970, 1, 1)).total_seconds()) - 4 == int((ttime - datetime(1970, 1, 1)).total_seconds()):
                    matches_el1.append(flir_data.iloc[time_f]['El1.Average'])
                    matches_el2.append(flir_data.iloc[time_f]['El2.Average'])
                    new_time = time_f  # Define new start point

                # Break when you passed the second of time
                # Towards the end of the file the running process slows down
                elif int((time - datetime(1970, 1, 1)).total_seconds()) - 3 == int((ttime - datetime(1970, 1, 1)).total_seconds()):
                    start = new_time  # Update start time, safes running time
                    break
            # Calculate average values over one second
            if len(matches_el1) != 0:
                average_el1 = sum(matches_el1) / len(matches_el1)
                average_el2 = sum(matches_el2) / len(matches_el2)
            # Add values to the dataframe
                data_file.at[row, 'FLIR_forehead'] = average_el1
                data_file.at[row, 'FLIR_nose'] = average_el2
                print(f'{trial} done!')
                trial += 1

        missings = data_file.index[(data_file['FLIR_nose'] == 99.9) |(data_file['FLIR_forehead'] == 99.9)]
        for missing in missings:
            data_file.drop(missing, inplace=True)

    # Add column with reaction times
    print("Adding reaction times")
    data_file['reaction_times'] = ''
    for time in data_file['start_time']:
        index, = data_file.index[(data_file['start_time'] == time)]
        reaction_time = (data_file.at[index, 'end_time'] - time).total_seconds() * 1000
        data_file.at[index, 'reaction_times'] = reaction_time

    # Prep times for ibutton matches
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
        print(f"Processing data from {ibutton_name}")

        # Get temperature from 4 seconds before target presenting (shortest interval)
        if ibutton_name != "FF00000045298741":  # Skipping the room temperature
            data_file[ibutton_name] = 99.9
            for time in temp['Date/Time']:
                good_time = pd.to_datetime(time)
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

    # Uncomment when you want to De-mean temperature features
    # print("De-mean temperature features")
    # if FLIR:
    #     features = ['FLIR_forehead', 'FLIR_nose', 'CB000000452D7441', '4B0000004516B141', '7200000045201D41',
    #                 '76000000452C9741', 'F9000000452CCF41', '9A00000045146841']
    # else:
    #     features = ['CB000000452D7441', '4B0000004516B141', '7200000045201D41',
    #                 '76000000452C9741', 'F9000000452CCF41', '9A00000045146841']
    #
    # for feature in features:
    #     mean = sum(data_file[feature]) / len(data_file[feature])
    #     data_file["mean"] = mean
    #     print(mean)
    #     data_file[feature] = data_file[feature] - data_file['mean']

    # Calculate four DPGs
    print("Calculate DPG_finger-chest")
    data_file['DPG_finger-chest'] = data_file['4B0000004516B141'] - data_file['9A00000045146841']

    print("Calculate DPG_nose-forehead")
    data_file['DPG_nose-forehead'] = data_file['CB000000452D7441'] - data_file['F9000000452CCF41']

    print("Calculate DPG_pinna-mastoid")
    data_file['DPG_pinna-mastoid'] = data_file['76000000452C9741'] - data_file['7200000045201D41']

    if flir_data is not None:
        print("Calculate FLIR_DPG_nose-forehead")
        data_file['FLIR_DPG_nose-forehead'] = data_file['FLIR_nose'] - data_file['FLIR_forehead']

    # Add data from questionnaires
    print("Adding data from the questionnaires")
    questionnaire_folder = directory + '/Questionnaires/questionnaire_data.csv'
    questionnaire_file = pd.read_csv(questionnaire_folder)
    row_number = questionnaire_file.index[(questionnaire_file['PPID'] == participant_id)]
    if len(row_number) != 0:
        data_file['Gender'] = questionnaire_file.at[row_number[0], 'Gender']  # Male / Female
        data_file['Age'] = questionnaire_file.at[row_number[0], 'Age']        # Number
        data_file['MEQ_type'] = questionnaire_file.at[row_number[0], 'type']  # Morning / Evening / Intermediate
        data_file['PSQI'] = questionnaire_file.at[row_number[0], 'total_score_PSQI']  # Float score on PSQI

    # Safe file to a csv
    data_file.to_csv(r'/Users/roos/Data/final_trials/trials' + participant_id + '.csv', index=False, header=True)
    # Keep track of participants
    i += 1
