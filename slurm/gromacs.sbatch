#!/bin/bash
#SBATCH --job-name=gromacs-threadmpi
#SBATCH --exclusive
#SBATCH --output=/shared/logs/%x_%j.out
#SBATCH -N 2
#SBATCH -n 96
NTOMP=1

mkdir -p /shared/jobs/${SLURM_JOBID}
cd /shared/jobs/${SLURM_JOBID}

spack load gromacs
module load openmpi

set -x
time mpirun -np ${SLURM_NTASKS} gmx_mpi mdrun -ntomp ${NTOMP} -s /shared/input/gromacs/benchRIB.tpr -resethway
