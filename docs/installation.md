# Installation Guide for GROMACS Deployment Tool

This guide provides step-by-step instructions for installing and setting up the GROMACS Deployment Tool on your system. Follow these instructions to get started.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.6 or higher
- Terraform
- AWS CLI (configured with appropriate permissions)

## Installation Steps

1. **Clone the Repository**

   Start by cloning the GROMACS Deployment Tool repository to your local machine. Open a terminal and run the following command:
   ```bash
   git clone https://github.com/your-repository/gromacs.git
   ```

2. **Navigate to the Project Directory**

   Change into the project directory with:
   ```bash
   cd gromacs
   ```

3. **Install Python Dependencies**

   Install the required Python dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Terraform**

   Navigate to the `terraform` directory within the project and initialize Terraform:
   ```bash
   cd terraform
   terraform init
   ```

5. **Deploy Infrastructure**

   Apply the Terraform configuration to deploy the necessary infrastructure. You will be prompted to confirm the action:
   ```bash
   terraform apply
   ```

   Type `yes` when prompted to proceed with the deployment.

6. **Configure GROMACS**

   After the infrastructure is deployed, update the GROMACS configuration file (`config/gromacs-config-multi-queue.yaml`) with the output values from Terraform (e.g., `subnet_id`, `vpc_id`).

7. **Run the GROMACS Deployment Tool**

   Return to the root directory of the project and run the deployment tool with the necessary arguments. For example, to deploy resources and create a cluster:
   ```bash
   python gromacs.py --deploy --terraform-directory ./terraform --gromacs-config ./config/gromacs-config-multi-queue.yaml
   ```

## Cleanup

To delete the resources created by the GROMACS Deployment Tool, run the following command in the `terraform` directory:
```bash
terraform destroy
```

