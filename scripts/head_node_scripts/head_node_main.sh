#!/bin/bash

# Define the SSH connection details
HEAD_NODE_IP="your.head.node.ip"
USER="your_username"
PEM_KEY_PATH="/path/to/your/key.pem"

# Define the scripts to execute on the head node
SCRIPTS_TO_RUN=("script1.sh" "script2.sh" "script3.sh")

# Loop through each script and execute it remotely
for script in "${SCRIPTS_TO_RUN[@]}"; do
    echo "Executing $script on the head node..."
    ssh -i "$PEM_KEY_PATH" "$USER@$HEAD_NODE_IP" "bash -l -c '~/path/to/scripts/$script'"
done

echo "All scripts executed."