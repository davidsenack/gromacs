#!/bin/bash

# Check for necessary dependencies
dependencies=("git" "wget" "unzip" "terraform" "pcluster")

for dep in "${dependencies[@]}"; do
  if ! command -v $dep &> /dev/null; then
    echo "$dep could not be found. Please install $dep."
    exit 1
  fi
done

# Clone the project repository
git clone https://github.com/your_project/gromacs.git /usr/local/bin/gromacs

# Make the main script executable
chmod +x /usr/local/bin/gromacs/gromacs.py

# Create a symbolic link to run the project with the command "gromacs"
ln -s /usr/local/bin/gromacs/gromacs.py /usr/local/bin/gromacs

echo "Installation complete. You can now run the project using the command 'gromacs'"
