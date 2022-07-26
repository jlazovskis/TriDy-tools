# TriDy-tools
Tools for creating new selection parameters and distributing featurisation tasks forthe [TriDy pipeline](https://github.com/JasonPSmith/TriDy).

### Setup

There are four pairs of `.py` and `.config` files. Each `.config` file is meant to be changed, then the `.py` file is meant to be executed with the `.config` file coming after it, for example:

    python create-bins.py create-bins.config
    
The tools do the following:
1. **create-bins.py**: Partitions the 31346 neurons into bins using a kd-tree, created by k chosen parameters. Number of bins is 2^n for the smallest integer n such that 31346/2^n <= (bin size)
 
2. **create-parameters.py**: Creates new "paramaters" for use in the TriDy pipeline. These are binary vectors of length 31346, with 1 in the positions of neurons to select, and 0 otherwise.

3. **create-runfiles.py**: Creates .sbatch and .json files for running TriDy, split into as many jobs as necessary. The TriDy package is necessary for this step, since temporary pipeline.py and toolbox.py files are created, to make sure that the new "parameters" are used. A bash `.sh` file containing all the commands to be executed is also created.

4. **collect-results.py**: Collects results created by running TriDy, and exports them in a dataframe.

The available parameters are given below, and are located in the `parameters.pkl` dataframe. Since there are so many, we split them up by type.

### Graph-theoretic parameters

| Name | Short name | Description |
| --- | --- | --- |
| tribe_size | ts | number of neurons in the closed neighbourhood of a neuron | 
| deg | deg | degree of the center of the closed neighbourhood |
| in_deg | ideg | number of incoming edges to the center |
| out_deg | odeg | number of outgoing edges from the center |
| rc | rc | number of pairs of reciprocal connections in the closed neighborhood |
| rc_chief | rcc | number of pairs of reciprocal connections in the neighbourhood with one end in the center |
| tcc | tcc | transitive clustering coefficient |
| fcc | fcc | classical (Fagiolo's) clustering coefficient |

### Topological parameters

| Name | Short name | Description |
| --- | --- | --- |
| dc2 | dc2 | 2nd density cefficient |
| dc3 | dc3 | 3rd density coefficient |
| dc4 | dc4 | 4th density coefficient | 
| dc5 | dc5 | 5th density coefficient |
| dc6 | dc6 | 6th density coefficient |
| nbc | nbc | normalised Betti coefficient |
| ec | ec | Euler characteristic | 
| 0simplices | 0simp | number of 0-simplices (nodes) in the closed neighbourhood |
| 1simplices | 1simp | number of 1-simplices (edges) in the closed neighbourhood |
| 2simplices | 2simp | number of 2-simplices (directed 3-cliques) in the closed neighbourhood |
| 3simplices | 3simp | number of 3-simplices (directed 4-cliques) in the closed neighbourhood |
| 4simplices | 4simp | number of 4-simplices (directed 5-cliques) in the closed neighbourhood |
| 5simplices | 5simp | number of 5-simplices (directed 6-cliques) in the closed neighbourhood |
| 6simplices | 6simp | number of 6-simplices (directed 7-cliques) in the closed neighbourhood |
| 7simplices | 7simp | number of 7-simplices (directed 8-cliques) in the closed neighbourhood |

### Spectral parameters

| Name | Short name | Description |
| --- | --- | --- |
| asg | asg | adjacency spectral gap (difference of two largest (by modulus) eigenvalues of the adjacency matrix) |
| asg_low | asl | smallest (by modulus) nonzero eigenvalue of the adjacency matrix |
| asg_radius | asr | largest (by modulus) nonzero eigenvalue of the adjacency matrix |
| tpsg | tpsg | transition probability spectral gap (difference of two largest (by modulus) eigenvalues of the transition probability matrix) |
| tpsg_low | tpsl | smallest (by modulus) nonzero eigenvalue of the transition probability matrix | 
| tpsg_radius | tpsr | largest (by modulus) nonzero eigenvalue of the transition probability matrix |
| tpsg_reversed | tpsgR | same, but edges are reversed |
| tpsg_reversed_low | tpsRl | same, but edges are reversed |
| tpsg_reversed_radius | tpsRr | same, but edges are reversed | 
| clsg | clsg | Chung Laplacian spectral gap (smallest (by modulus) nonzero eigenvalue of the Chung Laplacian) |
| clsg_high | clsh |  difference of two largest (by modulus) eigenvalues of the Chung Laplacian |
| clsg_radius | clsr | largest (by modulus) eigenvalue of the Chung Laplacian |
| blsg | blsg | Bauer Laplacian spectral gap (difference of two largest (by modulus) eigenvalues of the Bauer Laplacian) |
| blsg_low | blsl | smallest (by modulus) nonzero eigenvalue of the Bauer Laplacian | 
| blsg_radius | blsr | largest (by modulus) nonzero eigenvalue of the Bauer Laplacian | 
| blsg_reversed | blsgR | same, but edges are reversed |
| blsg_reversed_low | blsRl | same, but edges are reversed |
| blsg_reversed_radius | blsRr | same, but edges are reversed |
