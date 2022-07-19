# Load packages
print('Loading packages...', flush=True)
import json
from scipy.spation import kdtree

# Read config file
print('Reading configuration file..', flush=True)
config_address = sys.argv[1]
with open(config_address, 'r') as f:
    config_dict = json.load(f)

selection_parameters = config_dict['selection_parameters']    # A list of selection parameters by which to create a kd-tree. Note that the order matters

# Load selection parameter(s)

# Add and save noise

# Create kd-tree

# Save partition
