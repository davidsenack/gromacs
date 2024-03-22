#!/bin/bash

# Automates Spack installation and setup on Linux.
# Sets up Spack environment, clones Spack repo, and configures bashrc for Spack.
# Adds binary mirror for Spack packages, installs compilers and Gromacs.
# Fetches dataset for Gromacs, preparing system for scientific computation.

# Install Spack
sudo su
export SPACK_ROOT=/shared/spack
mkdir -p $SPACK_ROOT
git clone -c feature.manyFiles=true https://github.com/spack/spack $SPACK_ROOT
cd $SPACK_ROOT
exit
echo "export SPACK_ROOT=/shared/spack" >> $HOME/.bashrc
echo "source \$SPACK_ROOT/share/spack/setup-env.sh" >> $HOME/.bashrc
source $HOME/.bashrc
sudo chown -R $USER:$USER $SPACK_ROOT

spack mirror add binary_mirror  https://binaries.spack.io/releases/v0.18
spack buildcache keys --install --trust

# Install Intel Compiler 
spack install intel-oneapi-compilers@2022.0.2
sleep 300
spack load intel-oneapi-compilers
spack compiler find
spack unload

# Install Gromacs
spack install -v -j 8 gromacs@2022.2
sleep 180
spack load gromacs

# Fetch dataset
mkdir -p /shared/input/gromacs
mkdir -p /shared/logs
mkdir -p /shared/jobs

cd /shared/input/gromacs
#wget https://www.mpinat.mpg.de/benchMEM
#wget https://www.mpinat.mpg.de/benchPEP.zip
#wget https://www.mpinat.mpg.de/benchPEP-h.zip
wget https://www.mpinat.mpg.de/benchRIB.zip

# unzip
unzip bench*.zip