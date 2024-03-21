provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "gromacs_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "gromacs_vpc"
  }
}

resource "aws_subnet" "gromacs_subnet" {
  vpc_id     = aws_vpc.gromacs_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "gromacs_subnet"
  }
}

output "vpc_id" {
  value = aws_vpc.gromacs_vpc.id
}

output "subnet_id" {
  value = aws_subnet.gromacs_subnet.id
}