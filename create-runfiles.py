# Step 3 of 4: Create .sbatch and .json files for running TriDy

# Directories for stroing the results will be created.
# A file containing all the command to be executed is also created, named runfiles.sh. This can be executed with "bash runfiles.sh"
# Temporary pipeline.py and toolbox.py files are created as well, to make sure that the correct 'parameters' are used
# The content of the pipeline.py and toolbox.py files is assumed to be as in the latest version of TriDy

##
## Load packages
##

print('Loading packages', flush=True)
import pickle
import json
import sys
import subprocess
import os
import numpy as np
from functools import reduce

##
## Read config file
##

print('Reading configuration file', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

selection_parameters = config_dict['selection_parameters']        # List of selection parameters to use. Should match names of custom selection parameter binary arrays
feature_parameters = config_dict['feature_parameters']            # List of feature parameters to use. One collection of files will be created for each
feature_gaps = config_dict['feature_gaps']                        # List of feature parameter gaps to use. Must be of same length as feature_parameters. Irrelevant for all but spectral gaps
json_template = config_dict['json_template']                      # Template to use when creating configuration .json files
sbatch_template = config_dict['sbatch_template']                  # Template to use when creating .sbatch files to begin jobs
num_jobs = config_dict['num_jobs']                                # Number of jobs (=number of sbatch files) to split up featursation+classification task into
check_existing = config_dict['check_existing']                    # Check to see if some parameters have already been featurised. Default is False
bin_dir = config_dict['bin_dir']                                  # Location of bins (selection paramater partition). Necessary to know indices of jobs. Default is ./bins/
export_dir = config_dict['export_dir']                            # Where to export the runfiles. Default is ./runfiles/

created_file_counter = 0
created_directory_counter = 0

##
## Load parameter shortname dictionary
##

print('Loading parameter names', flush=True)
with open('data/parameters-shortnames.pickle', 'rb') as f:
    df_shortdict = pickle.load(f)

##
## Load function
##

print('Loading helper function', flush=True)

# Function to replace strings in files
# Modified from https://stackoverflow.com/questions/4128144
def file_string_replace(source_file, target_file, old_new_strings):

    # Safely read the input filename using 'with'
    with open(source_file) as f:
        s = f.read()
        for old_string,new_string in old_new_strings:
            if old_string not in s:
                print('"{old_string}" not found in {source_file}, exiting.'.format(**locals()))
                return

    # Safely write the changed content, if found in the file
    with open(target_file, 'w') as f:
        # print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        for old_string,new_string in old_new_strings:
            s = s.replace(old_string, new_string)
        f.write(s)

##
## Create folders and runfiles
##

for sparam in selection_parameters:

    # Load bins (partition) 
    expected_bins = bin_dir+'partition_'+sparam+'.npy'
    try:
        current_bins = np.load(expected_bins,allow_pickle=True)
        num_bins = len(current_bins)
        print('Selection parameter '+sparam+' has '+len(num_bins)+' bins', flush=True)
    except:
        print('Expected bin file '+expected_bins+' not found. Check bin_dir in conig file. Exiting.', flush=True)
        exit()

    # Iterate over feature parameters
    for findex,fparam in enumerate(feature_parameters):
        fshort = df_shortdict[fparam]
        fgap = feature_gaps[findex]
        assert fgap in ['high','low','radius'], 'Feature gap must be one of \'high\', \'low\', \'radius\'.' 
        current_name = sparam+'-'+fshort
        print(current_name, end='', flush=True)

        # Create folders
        os.mkdir('configs/'+current_name)
        os.mkdir('sbatches/'+current_name)
        os.mkdir('results/'+current_name)
        created_directory_counter += 3

        # Declare string replacements
        string_replacements = [('#SSHORT',sparam), ('#FPARAM',fparam), ('#FSHORT',fshort), ('#FGAP',fgap)]

        # Distribute jobs evenly
        chunk_size = num_bins//num_jobs
        chunks = [chunk_size]*num_jobs
        leftover_size = num_bins%chunk_size
        for i in range(leftover_size):
            chunks[i]+=1
        assert sum(chunks) == num_bins, 'Number of bins does not match sum of job sizes'
        chunks_sum = [sum(chunks[:k]) for k in range(len(chunks)+1)]

        for jobnum in range(num_jobs):
            print(' '+str(jobnum), end='', flush=True)
            string_replacements.append(('#JOBNUM',str(jobnum)))
            string_replacements.append(('#SPARAMS',reduce(lambda x,y: x+'\", \"'+y, [sparam+'-'+str(i) for i in range(chunks_sum[jobnum],chunks_sum[jobnum+1])])))

            # Create .json files
            file_string_replace(json_template, 'configs/'+current_name+'/'+str(jobnum)+'.json', string_replacements)
            created_file_counter += 1

            # Create .sbatch files
            file_string_replace(sbatch_template, 'sbatches/'+current_name+'/'+str(jobnum)+'.sbatch', string_replacements)
            created_file_counter += 1

            # Copy and modify toolbox.py file

            # Copy and modify pipeline.py file



##
## Open template files
##



# Read existing toolbox.py and pipeline.py files

# Insert new parameters and their location


##
## Print what was done
##

print('----------\nCreated '+str(created_file_counter)+' files', flush=True)
print('Created '+str(created_directory_counter)+' directories', flush=True)
print('All done, exiting', flush=True)
