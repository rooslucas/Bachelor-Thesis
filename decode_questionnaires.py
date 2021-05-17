import pandas as pd

demo_folder = "/Users/roos/Data/Questionnaires/Demographics_SleepQuestionnaire_v20210511.xlsx"
demo_file = pd.read_excel(demo_folder)
questionnaires_file = pd.DataFrame()

for PPID in demo_file['PPID']:
    row_number, = demo_file.index[demo_file['PPID'] == PPID]
    print(row_number)
    # print(demo_file.at[row_number, ])
    if row_number is not None:
        # Code component 1
        if demo_file.at[row_number, 6] == 'A':
            component_1 = 0
        elif demo_file.at[row_number, 6] == 'B':
            component_1 = 1
        elif demo_file.at[row_number, 6] == 'C':
            component_1 = 2
        elif demo_file.at[row_number, 6] == 'D':
            component_1 = 3
        else:
            component_1 = None

        # Code component 2
        if int(demo_file.at[row_number, '2_MinutesSleep']) <= 15:
            question_2 = 0
        elif int(demo_file.at[row_number, '2_MinutesSleep']) >= 16 & int(demo_file.at[row_number, '2_MinutesSleep']) <= 30:
            question_2 = 1
        elif int(demo_file.at[row_number, '2_MinutesSleep']) >= 31 & int(demo_file.at[row_number, '2_MinutesSleep']) <= 60:
            question_2 = 2
        elif int(demo_file.at[row_number, '2_MinutesSleep'] > 60):
            question_2 = 3
        else:
            question_2 = None

        if demo_file.at[row_number, '5A'] == 'A':
            question_5a = 0
        elif demo_file.at[row_number, '5A'] == 'B':
            question_5a = 1
        elif demo_file.at[row_number, '5A'] == 'C':
            question_5a = 2
        elif demo_file.at[row_number, '5A'] == 'D':
            question_5a = 3
        else:
            question_5a = None

        if (question_5a is not None) & (question_2 is not None):
            sum_2 = question_2 + question_5a
            if sum_2 == 0:
                component_2 = 0
            elif sum_2 == 1 or sum_2 == 2:
                component_2 = 1
            elif sum_2 == 3 or sum_2 == 4:
                component_2 = 2
            elif sum_2 == 5 or sum_2 == 6:
                component_2 = 3
        else:
            component_2 = None

        questionnaires_file['PSQI_component_1'] = component_1
        questionnaires_file['PSQI_component_2'] = component_2
        questionnaires_file['PSQI_component_3'] = ''
        questionnaires_file['PSQI_component_4'] = ''
        questionnaires_file['PSQI_component_5'] = ''
        questionnaires_file['PSQI_component_6'] = ''
        questionnaires_file['PSQI_component_7'] = ''
        questionnaires_file['PSQI_global_score'] = ''
