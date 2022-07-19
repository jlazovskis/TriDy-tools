# Step 2 of 4: Create 'paramaters' for use in the TriDy pipeline

# These are binary vectors of length 31346, with 1 in the positions of neurons to select, and 0 otherwise
# An input partition is necessary to create these parameters

# Load packages
print('Loading packages...', flush=True)
import json
import numpy as np

# Read config file
print('Reading configuration file..', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

selection_parameter_name = config_dict['selection_parameter_name']    # The name to give the new 'parameter'
bin_dir = config_dict['bin_dir']                                      # Location of the partition (made of bins) created in step 1. Default is ./bins/
export_dir = config_dict['export_dir']                                # Where to export the binary parameters. Default is ./parameters/

# Load partition

# Export binary parameters
