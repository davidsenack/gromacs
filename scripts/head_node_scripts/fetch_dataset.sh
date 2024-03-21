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
