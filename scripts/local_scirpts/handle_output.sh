#!/bin/bash

# Navigate to your Terraform directory
cd /home/david/github/davidsenack/public/gromacs/terraform

# Apply Terraform configuration
terraform apply -auto-approve

# Capture the outputs
VPC_ID=$(terraform output -raw vpc_id)
SUBNET_ID=$(terraform output -raw subnet_id)

# Path to your ParallelCluster configuration file
CONFIG_FILE="/home/david/github/davidsenack/public/gromacs/config/gromacs-config-multi-queue.yaml"

# Update the configuration file
sed -i "s/VpcIdPlaceholder/${VPC_ID}/g" $CONFIG_FILE
sed -i "s/SubnetIdPlaceholder/${SUBNET_ID}/g" $CONFIG_FILE

echo "Updated ParallelCluster configuration with VPC ID: ${VPC_ID} and Subnet ID: ${SUBNET_ID}"