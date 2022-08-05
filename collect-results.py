# Step 4 of 4: Collect results created by runfiles executed in step 3

# Reads .txt files created by running TriDy, exports them in a pandas dataframe
# Will check if dataframe exists, so as to not overwrite anything
# Will collect incomplete results and export a dataframe. Row number will correspond to bin index in partition

##
## Load packages
##

print('Loading packages', flush=True)
import json
import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd

##
## Read config file
##

print('Reading configuration file', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

overwrite_existing = config_dict['overwrite_existing']       # Whether or not to overwrite existing dataframes. Default is False.
collect_incomplete = config_dict['collect_incomplete']       # Whether or not to collect classification results from jobs that do not have all results. Default is False.
bin_dir = config_dict['bin_dir']                             # Directory to which bins have been exported. Only relevant if collect_incomplete is true. Default is ./bins/
results_dir = config_dict['results_dir']                     # Where the classification results are located. Default is ./results/
dataframe_dir = config_dict['dataframe_dir']                 # Where to export the dataframe. Default is ./dataframes/

created_file_counter = 0

##
## Load function
##

print('Loading helper function', flush=True)

# Function to extract numbers from TriDy results. Naive implementation
# Works for commit c622760 and for earlier verions
def extract_numbers(string):
    number_list = []
    current_index = 0
    current_number = ''
    at_number = False
    while current_index < len(string):
        if string[current_index] in ['0','1','2','3','4','5','6','7','8','9','.']:
            current_number += string[current_index]
            at_number = True
        elif at_number == True:
            number_list.append(float(current_number))
            current_number = ''
            at_number = False
        current_index += 1
    # Catch if number at the end
    if at_number == True:
        number_list.append(float(current_number))
    return number_list

##
## Get names of results to collect
##

paramater_names = [observed[0].split(results_dir)[1] for observed in os.walk(results_dir)][1:]
if not overwrite_existing:
    already_computed = [filename.split('.')[0] for filename in list(os.walk(dataframe_dir))[0][2]]
    for param in already_computed:
        if param in paramater_names:
            paramater_names.remove(param)

##
## Find existing text files
##

for param in paramater_names:
    print(param, flush=True)
    current_directory = results_dir+param+'/'
    current_files = [filename for filename in list(os.walk(current_directory))[0][2] if filename[-4:] == '.txt']
    print('Found '+str(len(current_files))+' text files to read', flush=True)

    if current_files != []:
        current_dict = {'bin_number':[], 'cv_acc':[], 'cv_err':[], 'test_acc':[], 'test_err':[]}
        for file in current_files:
            f = open(current_directory+file,'r')
            lines = f.readlines()
            f.close()

            for line_index,line in enumerate(lines):
                if line[:2].lower() == 'cv':
                    current_bin = int(lines[line_index-1].split('-')[-1])
                    current_numbers = extract_numbers(line)
                    current_dict['bin_number'].append(current_bin)
                    current_dict['cv_acc'].append(current_numbers[0])
                    current_dict['cv_err'].append(current_numbers[1])
                    current_dict['test_acc'].append(current_numbers[2])
                    current_dict['test_err'].append(current_numbers[3])

        print('Read '+str(len(current_dict['bin_number']))+' classification results', flush=True)
        if not collect_incomplete:
            sparam = param.split('-')[0]
            expected_bins = bin_dir+'partition_'+sparam+'.npy'
            try:
                current_bins = np.load(expected_bins,allow_pickle=True)
                num_bins = len(current_bins)
            except:
                print('Expected bin file '+expected_bins+' not found. Check bin_dir in config file. Exiting.', flush=True)
                exit()

        if (not collect_incomplete) and (num_bins != len(current_dict['bin_number'])):
            print('This is less than complete number ('+str(num_bins)+'), skipping', flush=True)
        else:
            df = pd.DataFrame.from_dict(current_dict)
            target_file = Path(dataframe_dir+param+'.pkl')
            assert not target_file.is_file(), 'Dataframe file exists, but config file says to not overwrite. Delete or rename dataframe, or change config file.'
            df.to_pickle(target_file)
            created_file_counter += 1

    else:
        print('No results exist, skipping', flush=True)

##
## Print what was done
##

print('----------\nCreated '+str(created_file_counter)+' files', flush=True)
print('All done, exiting', flush=True)


