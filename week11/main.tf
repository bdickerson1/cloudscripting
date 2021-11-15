terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_key_pair" "ssh-key" {
  key_name    = "ssh-key"
  public_key  = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDIb38w77JAnXOeaZJzcu2cprjPp8W4amb0WLGMqfwWxw7WX3ujaGmC/xPJIDKuVHcslqvUxS11mOIUVo04Aw57snRZO47h0+GKU56QO3dckY1ZN5AeGEH9mDrp6Q86FG2+AWnfy1hZZ6My9/ScIyQceKyu8B3Gic/SCrukETQ0YqUuQUVmjSwp/mJ5zfh8BxL+/Ec6erDqq1Uu0LilmjaJUcsD4s9VSwtBV44X2gWPNADBdLhPQCoIsD+zaioQGgqrMSihDr6LdOeoVu7pCp/mGIeARDBzW4ZIZBte1UJRlQrDUl3KZE6zQC3YHSEB9ybYkAUnw+suwj72IdtL8bjN"
}

resource "aws_instance" "app_server" {
  ami           = "ami-01cc34ab2709337aa"  
  instance_type = "t2.micro"
  tags = {
    Name = var.instance_name
  }
  key_name      = aws_key_pair.ssh-key.key_name
}
resource "aws_network_interface_sg_attachment" "sg_attachment" {
  security_group_id     = aws_security_group.web-sg.id
  network_interface_id  = aws_instance.app_server.primary_network_interface_id
}

resource "aws_security_group" "web-sg" {
  name = "web-sg"
    ingress {
      from_port = 22
      to_port = 22
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
      from_port = 0
      to_port = 0
      protocol = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
