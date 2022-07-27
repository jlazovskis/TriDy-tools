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
import numpy as np
from functools import reduce

##
## Read config file
##

print('Reading configuration file', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

selection_parameter_name = config_dict['selection_parameter_name']    # The name to give the new 'parameter'. Should be short names, joined by underscore
config_template = config_dict['config_template']                      # Template to use when creating configuration .json files
sbatch_template = config_dict['sbatch_template']                      # Template to use when creating .sbatch files to begin jobs
feature_parameters = config_dict['feature_parameters']                # List of feature parameters to use. One collection of files will be created for each
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

# https://stackoverflow.com/questions/4128144
def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        # print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)

##
## Create runfiles
##

for fparam in feature_parameters:


##
## Open template files
##



# Read existing toolbox.py and pipeline.py files

# Insert new parameters and their location

