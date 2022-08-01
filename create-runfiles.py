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

selection_parameters = config_dict['selection_parameters']            # List of selection parameters to use. Should be short names, joined by underscore
feature_parameters = config_dict['feature_parameters']                # List of feature parameters to use. One collection of files will be created for each
config_template = config_dict['config_template']                      # Template to use when creating configuration .json files
sbatch_template = config_dict['sbatch_template']                      # Template to use when creating .sbatch files to begin jobs
num_jobs = config_dict['num_jobs']                                    # Number of jobs (=number of sbatch files) to split up featursation+classification task into
check_existing = config_dict['check_existing']                        # Check to see if some parameters have already been featurised. Default is False
export_dir = config_dict['export_dir']                                # Where to export the runfiles. Default is ./runfiles/


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
def inplace_change(filename, old_new_strings):

    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        for old_string,new_string in old_new_strings:
            if old_string not in s:
                print('"{old_string}" not found in {filename}, exiting.'.format(**locals()))
                return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        # print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        for old_string,new_string in old_new_strings:
            s = s.replace(old_string, new_string)
        f.write(s)

##
## Create folders and runfiles
##

for fparam in feature_parameters:
    fshort = df_shortdict[fparam]
    for sparam in selection_parameters:
        print(fshort+' '+sparam, end='', flush=True)

        # Create folders
        subprocess.run(['mdir'])
        for jobnum in range(num_jobs):
            print(' '+str(jobnum), end='', flush=True)



##
## Open template files
##



# Read existing toolbox.py and pipeline.py files

# Insert new parameters and their location

