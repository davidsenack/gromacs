import os
import subprocess
import time


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


def delete_resources(cluster_name, terraform_directory):
    """Delete AWS ParallelCluster and Terraform resources."""
    # Delete AWS ParallelCluster
    subprocess.run([
        "pcluster", "delete-cluster", "--cluster-name", cluster_name
    ], check=True)
    print(f"AWS ParallelCluster {cluster_name} deletion initiated successfully.")

    # Wait for ParallelCluster deletion to complete
    # This is a placeholder for waiting logic. Adjust according to actual needs.
    time.sleep(300)  # Adjust the sleep time as necessary

    # Navigate to Terraform directory
    os.chdir(terraform_directory)

    # Delete Terraform resources
    subprocess.run(["terraform", "destroy", "-auto-approve"], check=True)
    print("Terraform resources deletion initiated successfully.")


def check_terraform_resources(terraform_directory):
    """Check if there are any Terraform resources still running."""
    os.chdir(terraform_directory)
    result = subprocess.run(["terraform", "state", "list"], capture_output=True, text=True)
    if result.stdout.strip():
        print("Warning: There are still Terraform resources running.")
    else:
        print("No Terraform resources are running.")


def check_pcluster_deletion(cluster_name):
    """Check if the AWS ParallelCluster is fully deleted."""
    result = subprocess.run(["pcluster", "describe-cluster", "--cluster-name", cluster_name], capture_output=True, text=True)
    if "ClusterStatus: DELETE_COMPLETE" in result.stdout:
        print(f"AWS ParallelCluster {cluster_name} is fully deleted.")
    else:
        print(f"Warning: AWS ParallelCluster {cluster_name} deletion may not be complete.")
