# Step 1 of 4: Create k-dimensional bins of neurons, using k selection paramaters and a kd-tree

# Number of bins is dependent on configuration file, which specifies bin size
# Number of bins is 2^n for the smallest integer n such that 31346/2^n <= (bin size) 

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
