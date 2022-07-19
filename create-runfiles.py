# Step 3 of 4: Create .sbatch and .json files for running TriDy

# A file containing all the command to be executed is also created, named runfiles.sh. This can be executed with "bash runfiles.sh"
# Temporary pipeline.py and toolbox.py files are created as well, to make sure that the correct 'parameters' are used
# The content of the pipeline.py and toolbox.py files is assumed to be as in the latest version of TriDy

# Load packages
print('Loading packages...', flush=True)
import json
import subprocess
import numpy as np

# Read config file
print('Reading configuration file..', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

config_template = config_dict['config_template']             # Template to use when creating configuration .json files
sbatch_template = config_dict['sbatch_template']             # Template to use when creating .sbatch files to begin jobs
num_jobs = config_dict['num_jobs']                           # Number of jobs (=number of sbatch files) to split up featursation+classification task into
check_existing = config_dict['check_existing']               # Check to see if some parameters have already been featurised. Default is False
export_dir = config_dict['export_dir']                       # Where to export the runfiles. Default is ./runfiles/

# Open template files

# Create runfiles

# Read existing toolbox.py and pipeline.py files

# Insert new parameters and their location

