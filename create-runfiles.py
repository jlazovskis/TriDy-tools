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
json_template = config_dict['json_template']                      # Template to use when creating configuration .json files
sbatch_template = config_dict['sbatch_template']                  # Template to use when creating .sbatch files to begin jobs
num_jobs = config_dict['num_jobs']                                # Number of jobs (=number of sbatch files) to split up featursation+classification task into
check_existing = config_dict['check_existing']                    # Check to see if some parameters have already been featurised. Default is False
only_featurise = config_dict['only_featurise']                    # If true, only creates the feature vectors and does not classify. Useful when repeating long jobs.
bin_dir = config_dict['bin_dir']                                  # Location of bins (selection paramater partition). Necessary to know indices of jobs. Default is ./bins/
parameter_dir = config_dict['parameter_dir']                      # Location of parameters created in step 2. Default is ./parameters/
tridy_dir = config_dict['tridy_dir']                              # Location of TriDy package as it is on github. Default is ./../TriDy/
runfile_dir = config_dict['runfile_dir']                          # Where to export the runfiles. Default is ./runfiles/
results_dir = config_dict['results_dir']                          # Where the classification results are located. Default is ./results/

# Get feature gaps from names
feature_gaps = []
for p in feature_parameters:
    if (p == "asg") or (p == "asg_high"):
        feature_gaps.append("high")
    elif (p == "tpsg") or (p == "tpsg_high"):
        feature_gaps.append("high")
    elif (p == "tpsg_reversed") or (p == "tpsg_reversed_high"):
        feature_gaps.append("high")
    elif (p == "clsg") or (p == "clsg_low"):
        feature_gaps.append("low")
    elif (p == "blsg") or (p == "blsg_high"):
        feature_gaps.append("high")
    elif (p == "blsg_reversed") or (p == "blsg_reversed_high"):
        feature_gaps.append("high")
    elif "high" in p:
        feature_gaps.append("high")
    elif "low" in p:
        feature_gaps.append("low")
    elif "radius" in p:
        feature_gaps.append("radius")
    else:
        feature_gaps.append("")

created_file_counter = 0
created_directory_counter = 0

##
## Load parameter shortname dictionary
##

print('Loading parameter names', flush=True)
with open('data/parameters-shortnames.pickle', 'rb') as f:
    df_shortdict = pickle.load(f)

# Dictionary for translating to pipeline names
fparam_to_pipename = {"fcc":"ccc"}
for name in ["ec","tribe_size","deg","in_deg","out_deg","rc","rc_chief","tcc","nbc","dc2","dc3","dc4","dc5","dc6","binary"]:
    fparam_to_pipename[name] = name
for spectrum in ["asg","tpsg", "tpsg_reversed", "clsg", "blsg", "blsg_reversed"]:
    for gap in ["", "_high", "_low", "_radius"]:
        fparam_to_pipename[spectrum+gap] = spectrum

##
## Load function
##

print('Loading helper function', flush=True)

# Function to replace strings in files
# Modified from https://stackoverflow.com/questions/4128144
def file_string_replace(source_file, target_file, old_new_strings, verbose=False):

    # Safely read the input filename using 'with'
    with open(source_file) as f:
        s = f.read()
        if verbose:
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
        print('Selection parameter '+sparam+' has '+str(num_bins)+' bins', flush=True)
    except:
        print('Expected bin file '+expected_bins+' not found. Check bin_dir in config file. Exiting.', flush=True)
        exit()

    # Iterate over feature parameters
    for findex,fparam in enumerate(feature_parameters):
        try:
            fshort = df_shortdict[fparam]
        except:
            fshort = df_shortdict[reduce(lambda x,y: x+'_'+y,fparam.split('_')[:-1])]
        fgap = feature_gaps[findex]
        assert fgap in ['', 'high','low','radius'], 'Feature gap must be one of \'\', \'high\', \'low\', \'radius\'.' 
        current_name = sparam+'-'+fshort
        print(current_name, flush=True)

        # Create folders
        for parent_dir in ['configs','sbatches','results']:
            try:
                os.mkdir(parent_dir+'/'+current_name)
                created_directory_counter += 1
            except:
                pass

        # Create list of vectors to featurise
        if check_existing:
            print('Searching for vectors not yet featurised. ', end='', flush=True)
            missing_vectors = []
            call = subprocess.run(['ls','/gpfs/bbp.cscs.ch/home/lazovski/TriDy-tools'+results_dir[1:]+current_name+'/'],stdout = subprocess.PIPE)
            out = call.stdout.decode('utf-8').split('\n')
            for i in range(num_bins):
                if sparam+'-'+str(i)+'_feature_vectors.npy' not in out:
                    missing_vectors.append(i)
        else:
            missing_vectors = list(range(num_bins))
        num_bins_real = len(missing_vectors)
        print('Found '+str(num_bins_real)+' vectors. ', end='', flush=True)

        if num_bins_real > 0:

            # Distribute jobs evenly
            chunk_size = num_bins_real//num_jobs
            chunks = [chunk_size]*num_jobs
            leftover_size = num_bins_real%num_jobs
            for i in range(leftover_size):
                chunks[i]+=1
            assert sum(chunks) == num_bins_real, 'Number of expected bins ('+str(num_bins_real)+') does not match sum of job sizes ('+str(sum(chunks))+')'
            chunks_sum = [sum(chunks[:k]) for k in range(len(chunks)+1)]
            job_list = [missing_vectors[chunks_sum[job_num]:chunks_sum[job_num+1]] for job_num in range(num_jobs)]

            # Inform user of status
            if num_bins_real < num_jobs:
                job_list = job_list[:num_bins_real]
                num_jobs = num_bins_real
            print('Splitting into '+str(num_jobs)+' jobs', flush=True)

            # Generate .sh file for easy execution of sbatch files
            f = open(runfile_dir+current_name+'.sh','w')

            for job_num in range(num_jobs):
                # Declare string replacements
                string_replacements = [('#SSHORT',sparam), ('#FPARAM',fparam_to_pipename[fparam]), ('#FSHORT',fshort), ('#FGAP',fgap)]

                string_replacements.append(('#JOBNUM',str(job_num)))
                string_replacements.append(('#SPARAMS',reduce(lambda x,y: x+'\", \"'+y, [sparam+'-'+str(i) for i in job_list[job_num]])))

                # Create .json files
                file_string_replace(json_template, 'configs/'+current_name+'/'+str(job_num)+'.json', string_replacements)
                created_file_counter += 1

                # Create .sbatch files
                file_string_replace(sbatch_template, 'sbatches/'+current_name+'/'+str(job_num)+'.sbatch', string_replacements)
                created_file_counter += 1

                # Write line to .sh file
                f.write('sbatch ../sbatches/'+current_name+'/'+str(job_num)+'.sbatch\n')

            # Close .sh file
            f.close()
            created_file_counter += 1

            # Reset number of jobs
            num_jobs = config_dict['num_jobs']

        else:
            print('Nothing to do, skipping', flush=True)

    print('Creating modified toolbox.py and pipeline.py files', flush=True)
    # Copy and modify toolbox.py file
    toolbox_replacements = [(
        # Custom selection parameter names in dictionary
        'param_dict_inverse = {',
        'for i in range('+str(num_bins)+'):\n    param_dict[\''+sparam+'-\'+str(i)]=\''+sparam+'-\'+str(i)\n\nparam_dict_inverse = {'
        ),(
        # Load custom selection parameters
        'param_files = [np.load(dir_export+\'individual_parameters/\'+param_dict_inverse[f]+\'.npy\',allow_pickle=True) for f in param_names]\n',
        'param_files = []\nfor f in param_names:\n    try:\n        param_files.append(np.load(dir_export+\'individual_parameters/\'+param_dict_inverse[f]+\'.npy\',allow_pickle=True))\n    except:\n        param_files.append(np.load(\'./../TriDy-tools'+parameter_dir[1:]+'\'+param_dict_inverse[f]+\'.npy\',allow_pickle=True))\n'
        )]

    file_string_replace(tridy_dir+'toolbox.py', runfile_dir+'toolbox-'+sparam+'.py', toolbox_replacements)
    created_file_counter += 1

    # Copy and modify pipeline.py file
    pipeline_replacements = [(
        # Open modified toolbox file
        'exec(open(\'toolbox.py\').read())',
        'exec(open(\'../TriDy-tools'+runfile_dir[1:]+'toolbox-'+sparam+'.py\').read())'
        ),(
        # Declare job number
        '\'bin_number\']\n',
        '\'bin_number\']\njob_order = config_dict[\'values\'][\'job_order\']\n'
        ),(
        # Insert job number into output file
        'output = open(savefolder + \'classification_accuracies_\'+feature_parameter+\'.txt\',\'w\')',
        'output = open(savefolder + \'classification_accuracies_\'+feature_parameter+\'_\'+str(job_order)+\'.txt\',\'w\')'
        )]
    # Remove classification step
    if only_featurise:
        pipeline_replacements.append(('classify()\n','# classify()\n'))

    file_string_replace(tridy_dir+'pipeline.py', runfile_dir+'pipeline-'+sparam+'.py', pipeline_replacements)
    created_file_counter += 1

##
## Print what was done
##

print('----------\nCreated '+str(created_file_counter)+' files', flush=True)
print('Created '+str(created_directory_counter)+' directories', flush=True)
print('All done, exiting', flush=True)
