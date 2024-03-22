import os
import subprocess
import sys

# TODO: import terraform_directory from main
from main import terraform_directory

# Delete the cluster
delete_cluster_cmd = "pcluster delete my-cluster-name --region us-east-1"
process = subprocess.run(delete_cluster_cmd, shell=True, text=True)
if process.returncode == 0:
    print("Cluster deletion initiated successfully.")
else:
    print("Failed to initiate cluster deletion.")
    sys.exit(1)

# Change to the Terraform directory
os.chdir(terraform_directory)

# Initialize and destroy Terraform resources
init_cmd = "terraform init"
destroy_cmd = "terraform destroy -auto-approve"
subprocess.run(init_cmd, shell=True, text=True)
process = subprocess.run(destroy_cmd, shell=True, text=True)
if process.returncode == 0:
    print("Terraform resources deletion initiated successfully.")
else:
    print("Failed to initiate Terraform resources deletion.")
    sys.exit(1)