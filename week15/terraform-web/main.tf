terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      #version = "~> 3.27"
    }
  }
  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = var.region
}

#lookup AZ availability
data "aws_availability_zones" "available" {
    state = "available"
}
#data "aws_vpc" "myVPC" {
#  myvpcid = module.vpc.vpc_id
#}

data "aws_ami" "amistuff" {
  owners = ["amazon"]
  most_recent = true
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}



module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "3.11.0"

  name = "Fall2021finalVPC"
  cidr = var.cidr

  azs = data.aws_availability_zones.available.zone_ids
  private_subnets = var.private_subnets
  public_subnets = var.public_subnets

  enable_nat_gateway = false
  enable_vpn_gateway = false

}

module "web-server-sg" {
  source = "terraform-aws-modules/security-group/aws"
  version = "4.7.0"

  name = "web-sg"
  description = "security group for webserver allow ALL traffic"
  vpc_id = module.vpc.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules = ["all-all"]

  egress_cidr_blocks = ["0.0.0.0/0"]
  egress_rules = ["all-all"]
}

module "ec2_instance" {
  source = "terraform-aws-modules/ec2-instance/aws"
  version = "3.3.0"

  name = "Ben-web-server"
  ami = data.aws_ami.amistuff.id 
  instance_type = "t2.micro"
  key_name = "vockey"
  vpc_security_group_ids = [module.web-server-sg.security_group_id]
  #vpc_security_group_ids = data.aws_security_group.web-sg.id
  subnet_id = "${element(module.vpc.public_subnets, 0)}"
  user_data = templatefile("${path.module}/init-script.sh", {
    file_content = "BEN DICKERSON"
    })
}


output "security_group_id" {
    description = "security group ID"
    value = module.web-server-sg.security_group_id
}

output "vpc_id" {
    description = "security group ID"
    value = module.vpc.vpc_id
}

output "public_subnets" {
    description = "public subnet IDs"
    value = [module.vpc.public_subnets]
}

output "instance_public_ip" {
description = "Public IP address of the EC2 instance"
value = module.ec2_instance.public_ip
}