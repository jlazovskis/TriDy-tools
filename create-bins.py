# Step 1 of 4: Create k-dimensional bins of neurons, using k selection paramaters and a kd-tree

# Number of bins is dependent on configuration file, which specifies bin size
# Number of bins is 2^n for the smallest integer n such that 31346/2^n <= (bin size) 

##
## Load packages
##

print('Loading packages ...', flush=True)
import numpy as np
import pandas as pd
import json
import pickle
from scipy.spatial import kdtree
print('... done', flush=True)

nnum = 31346

##
## Read config file
##

print('Reading configuration file..', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

selection_parameters = config_dict['selection_parameters']    # A list of selection parameters by which to create a kd-tree. Note that the order matters.
add_noise = config_dict['add_noise']                          # A boolean list of the same length as above, indicating to which parameters noise should be added. If shorter, assume True.
binsize_target = config_dict['binsize_target']                # The target leaf size for the kd-tree. Not guaranteed by default. Will not exceed this if unique values.
overwrite_existing = config_dict['overwrite_existing']        # Wether or not to overwrite existing bins (and noise). Default is False.
export_dir = config_dict['export_dir']                        # Directory to which bins will be exported, as a single (ragged) .npy array.
print('... successfully loaded '+str(len(config_dict.keys()))+' arguments', flush=True)

##
## Auxiliary functions
##

print('Loading functions ...', flush=True)
# Reutrns partition. Modified from code suggested by Michael W. Reimann
def return_partition(tree, verbose=True, save_split=False):
    global partition_size
    global split_order
    partition_size = []
    split_order = []
    leaf_size(tree.tree, '')
    if verbose:
        print('Partitioned into {0} bins, of {1} different sizes ({2} to {3})'.format(
            len(partition_size),
            len(np.unique(np.array(partition_size))),
            min(partition_size),
            max(partition_size)
        ))
    partition_size_sums = [sum(partition_size[:k]) for k in range(len(partition_size)+1)]
    split = [tree.indices[partition_size_sums[k]:partition_size_sums[k+1]] for k in range(len(partition_size))]
    if save_split:
        return (split, split_order)
    else:
        return split

def leaf_size(tree, order_string):
    if hasattr(tree, "greater"):
        leaf_size(tree.less, order_string+'l')
        leaf_size(tree.greater, order_string+'g')
    else:
        partition_size.append(tree.children)
        split_order.append(order_string)

print('... done', flush=True)

##
## Load selection parameter(s)
##

print('Loading selection parameters ...', flush=True)
df = pd.read_pickle('parameters.pkl')
parameters = []
for s in selection_parameters:
    assert s in df.columns, 'Input parameter \''+s+'\' not found in dataframe parameters.pkl column names'
    parameters.append(df[s])

with open('parameters-shortnames.pickle', 'rb') as f:
    df_shortdict = pickle.load(f)

print('... successfully loaded '+len(parameters)+' parameters', flush=True)

##
## Add and save noise
##

print('Adding noise to selection parameters', flush=True)
for i,s in enumerate(selection_parameters):
    print('Parameter 1 ('+s+'): ', end='', flush=True)
    current_parameter = parameters[i]
    current_short = df_shortdict[s]
    ratio = np.round(len(np.unique(current_parameter))/nnum,3)
    print('unique to all ratio is '+str(ratio), flush=True)
    if add_noise[i]:
        # Create noise
        current_sorted = np.sort(np.unique(current_parameter))
        current_diff = np.diff(s_sorted)
        current_min = np.min(current_diff)
        current_noise = np.array([(k-.5)*current_min for k in np.random.rand(nnum)])
        current_new = np.array([current_parameter[k]+current_noise[k] for k in range(len(current_parameter))])

        # Check unique ratio is 1
        parameters[i] = current_new
        ratio = np.round(len(np.unique(current_new))/nnum,3)
        print('Noise added. New unique to all ratio is '+str(ratio), flush=True)

        # Save noise
        print('Saving noise ... ', flush=True)
        if overwrite_existing:
            np.save(export_dir+'noise_'+current_short+'.npy', current_noise)
        else:
            try:
                existing_noise = np.load(export_dir+'noise_'+current_short+'.npy', allow_pickle=True)
                assert False, 'Noise file exists, but config file says to not overwrite. Delete noise file or change config file.'
            except:
                np.save(export_dir+'noise_'+current_short+'.npy', current_noise)
        print('... done', flush=True)
    else:
        print('No noise added', flush=True)
print('... done adding noise', flush=True)

##
## Create kd-tree
##

print('Creating kd-tree in '+str(len(selection_parameters))+' dimensions ...', flush=True)


# Save partition
