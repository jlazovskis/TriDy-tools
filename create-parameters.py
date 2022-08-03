# Step 2 of 4: Create 'paramaters' for use in the TriDy pipeline

# These are binary vectors of length 31346, with 1 in the positions of neurons to select, and 0 otherwise
# An input partition is necessary to create these parameters

##
## Load packages
##

print('Loading packages', flush=True)
import json
import sys
import numpy as np

nnum = 31346

##
## Read config file
##

print('Reading configuration file', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

selection_parameter_name = config_dict['selection_parameter_name']    # The name to give the new 'parameter'. Should be short names, joined by underscore
bin_dir = config_dict['bin_dir']                                      # Location of the partition (made of bins) created in step 1. Default is ./bins/
parameter_dir = config_dict['parameter_dir']                          # Where to export the binary parameters. Default is ./parameters/

##
## Load partition
##

print('Loading partition', flush=True)
partition = np.load(bin_dir+'partition_'+selection_parameter_name+'.npy', allow_pickle=True)

##
## Export binary parameters
##

print('Creating binary parameter vectors', flush=True)
for i,b in enumerate(partition):
    current_parameter = np.zeros(nnum,dtype=int)
    for neuron in b:
        current_parameter[neuron] = 1
    np.save(parameter_dir + selection_parameter_name + '-' + str(i) + '.npy',current_parameter)

print('All done', flush=True)
