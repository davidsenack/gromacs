import os
import subprocess
import sys


def create_pcluster(terraform_directory):
    """Create AWS ParallelCluster with Terraform configuration."""
    # Navigate to Terraform directory
    os.chdir(terraform_directory)

    # Initialize and apply Terraform configuration
    subprocess.run(["terraform", "init"], check=True)
    subprocess.run(["terraform", "apply", "-auto-approve"], check=True)

    # Get subnet_id from Terraform output
    subnet_id = subprocess.run(
        ["terraform", "output", "-raw", "subnet_id"], 
        capture_output=True, text=True
    ).stdout.strip()

    # Run handle_output.sh with subnet_id
    subprocess.run(["/path/to/handle_output.sh", subnet_id], check=True)

    # Create AWS ParallelCluster
    subprocess.run(["pcluster", "create-cluster", "--cluster-name", "gromacs", "--cluster-configuration", "/path/to/your/gromacs-config-multi-queue.yaml"], check=True)


def delete_cluster(terraform_directory):
    """Delete AWS ParallelCluster and Terraform resources."""
    # Delete the cluster
    process = subprocess.run(["pcluster", "delete", "my-cluster-name", "--region", "us-east-1"], check=True, text=True)
    if process.returncode == 0:
        print("Cluster deletion initiated successfully.")
    else:
        print("Failed to initiate cluster deletion.")
        sys.exit(1)

    # Change to the Terraform directory
    os.chdir(terraform_directory)

    # Destroy Terraform resources
    subprocess.run(["terraform", "init"], check=True, text=True)
    process = subprocess.run(["terraform", "destroy", "-auto-approve"], check=True, text=True)
    if process.returncode == 0:
        print("Terraform resources deletion initiated successfully.")
    else:
        print("Failed to initiate Terraform resources deletion.")
        sys.exit(1)


def update_parallelcluster_config(terraform_directory, gromacs_config_yaml):
    """Update AWS ParallelCluster configuration with Terraform outputs."""
    # Navigate to Terraform directory
    os.chdir(terraform_directory)

    # Apply Terraform configuration
    subprocess.run(["terraform", "apply", "-auto-approve"], check=True)

    # Capture Terraform outputs
    vpc_id = subprocess.run(["terraform", "output", "-raw", "vpc_id"], capture_output=True, text=True).stdout.strip()
    subnet_id = subprocess.run(["terraform", "output", "-raw", "subnet_id"], capture_output=True, text=True).stdout.strip()

    # Update ParallelCluster configuration file
    with open(gromacs_config_yaml, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('VpcIdPlaceholder', vpc_id).replace('SubnetIdPlaceholder', subnet_id)
    with open(gromacs_config_yaml, 'w') as file:
        file.write(filedata)

    print(f"Updated ParallelCluster configuration with VPC ID: {vpc_id} and Subnet ID: {subnet_id}")


def execute_remote_scripts():
    import subprocess

    # Define the SSH connection details
    HEAD_NODE_IP = "your.head.node.ip"
    USER = "your_username"
    PEM_KEY_PATH = "/path/to/your/key.pem"

    # Define the scripts to execute on the head node
    SCRIPTS_TO_RUN = ["script1.sh", "script2.sh", "script3.sh"]

    # Loop through each script and execute it remotely
    for script in SCRIPTS_TO_RUN:
        print(f"Executing {script} on the head node...")
        subprocess.run(["ssh", "-i", PEM_KEY_PATH, f"{USER}@{HEAD_NODE_IP}", "bash -l -c '~/path/to/scripts/{}'".format(script)])

    print("All scripts executed.")
    