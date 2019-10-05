#!/bin/bash
 
#Submit this script with: sbatch run_center.sh

#SBATCH --time=1:00:00   # walltime
#SBATCH --ntasks=192   # number of processor cores (i.e. tasks)
#SBATCH --mem-per-cpu=1G   # memory per CPU core
#SBATCH -J “BOMEX_restart”   # job name
#SBATCH --mail-user=zhaoyi@caltech.edu   # email address
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
srun python main.py Bomex_restart.in
