# Step 4 of 4: Collect results created by runfiles executed in step 3

# Reads .txt files created by running TriDy, exports them in a pandas dataframe
# Will check if dataframe exists, so as to not overwrite anything
# Will collect incomplete results and export a dataframe. Row number will correspond to bin index in partition

# Load packages
print('Loading packages...', flush=True)
import json
import subprocess
import numpy as np
import pandas as pd

# Read config file
print('Reading configuration file..', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

results_dir = config_dict['results_dir']                     # Where the classification results are located. Default is ./results/
export_dir = config_dict['export_dir']                       # Where to export the dataframe. Default is ./

# Look for all .txt files in results folder

# Read each file and find the numbers

# Export dataframe

