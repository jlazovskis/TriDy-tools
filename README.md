# TriDy-tools
Tools for creating new selection parameters and distributing featurisation tasks

### Setup

There are four pairs of `.py` and `.config` files. Each `.config` file is meant to be changed, then the `.py` file is meant to be executed with the `.config` file coming after it, for example:

    python create-bins.py create-bins.config
    
The tools do the following:
1. *create-bins.py*: 
2. *create-parameters.py*:
3. *crate-runfiles.py*:
4. *collect-results.py*:

### Parameters

The available parameters are given below, and are located in the `parameters.pkl` dataframe. Since there are so many, we split them up, first listing the graph-theoretic / topological parameters.

| Name | Short name | Description |
| --- | --- | --- |
| tribe_size | ts | number of neurons in the closed neighbourhood of a neuron | 
| deg | deg | degree of the center of the closed neighbourhood |
| in_deg | ideg | number of incoming edges to the center |
| out_deg | odeg | number of outgoing edges from the center |
| rc | rc | number of pairs of reciprocal connections in the closed neighborhood |
| rc_chief | rcc | number of pairs of reciprocal connections in the neighbourhood with one end in the center |
| tcc | tcc | transitive clustering coefficient |
| ccc | ccc | classical (Fagiolo's) clustering coefficient |
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

Next we list the spectral parameters.

| Name | Short name | Description |
| --- | --- | --- |
| asg | as | adjacency spectral gap (difference of two largest (by modulus) eigenvalues of the adjacency matrix) |
| asg_low | asl | smallest (by modulus) nonzero eigenvalue of the adjacency matrix |
| asg_radius | asr | largest (by modulus) nonzero eigenvalue of the adjacency matrix |
| tpsg | tps | transition probability spectral gap (difference of two largest (by modulus) eigenvalues of the transition probability matrix) |
| tpsg_low | tpsl | smallest (by modulus) nonzero eigenvalue of the transition probability matrix | 
| tpsg_radius | tpsr | largest (by modulus) nonzero eigenvalue of the transition probability matrix |
| tpsg_reversed | tpsR | same, but edges are reversed |
| tpsg_reversed_low | tpsRl | same, but edges are reversed |
| tpsg_reversed_radius | tpsRr | same, but edges are reversed | 
| clsg | cls | Chung Laplacian spectral gap (smallest (by modulus) nonzero eigenvalue of the Chung Laplacian) |
| clsg_high | clsh |  difference of two largest (by modulus) eigenvalues of the Chung Laplacian |
| clsg_radius | clsr | largest (by modulus) eigenvalue of the Chung Laplacian |
| blsg | bls | Bauer Laplacian spectral gap (difference of two largest (by modulus) eigenvalues of the Bauer Laplacian) |
| blsg_low | blsl | smallest (by modulus) nonzero eigenvalue of the Bauer Laplacian | 
| blsg_radius | blsr | largest (by modulus) nonzero eigenvalue of the Bauer Laplacian | 
| blsg_reversed | blsR | same, but edges are reversed |
| blsg_reversed_low | blsRl | same, but edges are reversed |
| blsg_reversed_radius | blsRr | same, but edges are reversed |
