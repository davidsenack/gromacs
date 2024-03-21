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