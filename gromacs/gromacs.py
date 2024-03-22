#!/usr/bin/python3

import os
import subprocess
import time
import argparse


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
    update_gromacs_config_with_terraform_output(
        terraform_directory, gromacs_config_yaml)

    return subnet_id


def update_gromacs_config_with_terraform_output(
        terraform_directory, gromacs_config_yaml):
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
    filedata = filedata.replace('VpcIdPlaceholder', vpc_id)\
        .replace('SubnetIdPlaceholder', subnet_id)
    with open(gromacs_config_yaml, 'w') as file:
        file.write(filedata)

    print(f"Updated GROMACS config with VPC ID: {vpc_id} and Subnet ID: {subnet_id}")


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
    print(f"AWS ParallelCluster {cluster_name} deletion initiated.")

    # Wait for ParallelCluster deletion to complete
    # This is a placeholder for waiting logic. Adjust as needed.
    time.sleep(300)  # Adjust the sleep time as necessary

    # Navigate to Terraform directory
    os.chdir(terraform_directory)

    # Delete Terraform resources
    subprocess.run(["terraform", "destroy", "-auto-approve"], check=True)
    print("Terraform resources deletion initiated successfully.")


def check_terraform_resources(terraform_directory):
    """Check if there are any Terraform resources still running."""
    os.chdir(terraform_directory)
    result = subprocess.run(["terraform", "state", "list"], 
                            capture_output=True, text=True)
    if result.stdout.strip():
        print("Warning: Terraform resources still running.")
    else:
        print("No Terraform resources are running.")


def check_pcluster_deletion(cluster_name):
    """Check if the AWS ParallelCluster is fully deleted."""
    result = subprocess.run(["pcluster", "describe-cluster", 
                             "--cluster-name", cluster_name], 
                            capture_output=True, text=True)
    if "ClusterStatus: DELETE_COMPLETE" in result.stdout:
        print(f"AWS ParallelCluster {cluster_name} is fully deleted.")
    else:
        print(f"Warning: AWS ParallelCluster {cluster_name} deletion incomplete.")


def main():
    parser = argparse.ArgumentParser(description="GROMACS Deployment Tool")

    parser.add_argument("--deploy", action="store_true",
                        help="Deploy resources and create cluster")
    
    parser.add_argument("--delete", action="store_true",
                        help="Delete cluster resources")
    
    parser.add_argument("--check-terraform", action="store_true", 
                        help="Check if Terraform resources are still running")
    
    parser.add_argument("--check-cluster", action="store_true", 
                        help="Check if AWS ParallelCluster is fully deleted")
    
    parser.add_argument("--terraform-directory", type=str,
                        help="Path to Terraform directory")
    
    parser.add_argument("--gromacs-config", type=str,
                        help="Path to GROMACS configuration file")
    
    parser.add_argument("--cluster-name", type=str, default="gromacs",
                        help="Name of the AWS ParallelCluster")
    
    parser.add_argument("--version", action="store_true",
                        help="Print version and exit")

    args = parser.parse_args()

    if args.deploy:
        if not args.terraform_directory or not args.gromacs_config:
            parser.error("--deploy requires --terraform-directory "
                         "and --gromacs-config.")
        deploy_terraform_resources(
            args.terraform_directory, args.gromacs_config)
        create_pcluster(args.gromacs_config)
    elif args.delete:
        if not args.terraform_directory:
            parser.error("--delete requires --terraform-directory.")
        delete_resources(args.cluster_name, args.terraform_directory)
    elif args.check_terraform:
        if not args.terraform_directory:
            parser.error("--check-terraform requires --terraform-directory.")
        check_terraform_resources(args.terraform_directory)
    elif args.check_cluster:
        check_pcluster_deletion(args.cluster_name)
    elif args.version:
        print("GROMACS v0.1")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    