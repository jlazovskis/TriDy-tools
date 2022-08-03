#!/bin/bash
#SBATCH -N 1 # number of nodes
#SBATCH -n 8 # number of cores
#SBATCH --mem 256G # memory pool for all cores
#SBATCH -o ../out-err/%j.out # STDOUT
#SBATCH -e ../out-err/%j.err # STDERR
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=1
#SBATCH --job-name=#SSHORT-#FSHORT-#JOBNUM
#SBATCH --account=proj9 
#SBATCH --partition=prod

cd '/gpfs/bbp.cscs.ch/home/lazovski/'
module load archive/2022-06
module load python/3.9.7
source werk/bin/activate

cd '/gpfs/bbp.cscs.ch/home/lazovski/TriDy/'
python '/gpfs/bbp.cscs.ch/home/lazovski/TriDy-tools/mainfiles/pipeline-#SSHORT.py' '/gpfs/bbp.cscs.ch/home/lazovski/TriDy-tools/configs/#SSHORT-#FSHORT/#JOBNUM.json'
