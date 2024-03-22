import os
import subprocess


def deploy_terraform_resources(terraform_directory, gromacs_config_yaml):
    """Deploy resources defined in the Terraform configuration."""
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
    update_gromacs_config_with_terraform_output(terraform_directory, gromacs_config_yaml)

    return subnet_id


def update_gromacs_config_with_terraform_output(terraform_directory, gromacs_config_yaml):
    """Update GROMACS configuration with Terraform outputs."""
    # Navigate to Terraform directory
    os.chdir(terraform_directory)

    # Capture Terraform outputs
    vpc_id = subprocess.run(
        ["terraform", "output", "-raw", "vpc_id"], 
        capture_output=True, text=True
    ).stdout.strip()
    subnet_id = subprocess.run(
        ["terraform", "output", "-raw", "subnet_id"], 
        capture_output=True, text=True
    ).stdout.strip()

    # Update GROMACS configuration file
    with open(gromacs_config_yaml, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('VpcIdPlaceholder', vpc_id).replace('SubnetIdPlaceholder', subnet_id)
    with open(gromacs_config_yaml, 'w') as file:
        file.write(filedata)

    print(f"Updated GROMACS configuration with VPC ID: {vpc_id} and Subnet ID: {subnet_id}")


def create_pcluster(gromacs_config_yaml):
    """Create AWS ParallelCluster using the updated GROMACS configuration."""
    # Create AWS ParallelCluster
    subprocess.run([
        "pcluster", "create-cluster", "--cluster-name", "gromacs",
        "--cluster-configuration", gromacs_config_yaml
    ], check=True)

    print("AWS ParallelCluster creation initiated successfully.")
