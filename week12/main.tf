terraform {
    backend "remote" {
        organization = "2021-Fall-terraform-scripting"
        workspaces {
            name = "Ben-Demo-Workspace"
        }
    }
    required_providers {
        aws = {
           source = "hashicorp/aws"
           version = "~> 3.27"
        }
    }
    required_version = ">= 0.14.9"
}

provider "aws" {
    profile = "default"
    region = "us-east-1"
}

data "aws_iam_role" "lab_role" {
    name = "LabRole"
}

resource "aws_lambda_function" "test_lambda"{
    filename = "startEC2.zip"
    function_name = "lambda_function_Ben_start"
    role = data.aws_iam_role.lab_role.arn
    runtime = "python3.9"
    handler = "startEC2.lambda_handler"
}