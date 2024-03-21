#!/bin/bash

# Step 1: Navigate to your Terraform directory
cd /path/to/your/terraform/directory

# Step 2: Initialize and apply Terraform configuration
terraform init && terraform apply -auto-approve

# Assuming the Terraform output you're interested in is named "subnet_id"
SUBNET_ID=$(terraform output -raw subnet_id)

# Step 3: Run the handle_output.sh script
# Assuming handle_output.sh takes the subnet ID as an argument
/path/to/handle_output.sh $SUBNET_ID

# Step 4: Create the AWS ParallelCluster
# Ensure the path to your YAML configuration file is correct
pcluster create-cluster --cluster-name gromacs --cluster-configuration /path/to/your/gromacs-config-multi-queue.yaml

# Note: Replace "/path/to/your/terraform/directory", "/path/to/handle_output.sh", and "/path/to/your/gromacs-config-multi-queue.yaml"
# with the actual paths in your environment.