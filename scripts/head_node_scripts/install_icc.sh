spack install intel-oneapi-compilers@2022.0.2
sleep 300
spack load intel-oneapi-compilers
spack compiler find
spack unload
