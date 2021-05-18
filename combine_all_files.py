# Script to combine all trials from all participants
import pandas as pd
import os, glob

directory = '/Users/roos/Data/Trials/'

all_files = glob.glob(os.path.join(directory, "*.csv"))
print(all_files)
df_all_files = (pd.read_csv(f, sep=',') for f in all_files)
print(df_all_files)
combined_files = pd.concat(df_all_files, ignore_index=True)
combined_files.to_csv(r'/Users/roos/Data/all_trials.csv', index=False, header=True)

# Combine all trials in one file
# trials_folder = directory + '/Trials'
# trials_list = os.listdir(trials_folder)
# all_trials = glob.glob(os.path.join(trials_folder, '*.csv'))
#
# combined_trials = pd.concat([pd.read_csv(f, delimiter='t', encoding='UTF-16') for f in all_trials])
# combined_trials.to_csv("r'/Users/roos/Data/alltrials.csv")
