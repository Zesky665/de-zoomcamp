terraform {
  cloud {
    organization = "ZhareC"

    workspaces {
      name = "100dayofde"
    }
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.38.0"
    }
  }
}

# // BEGIN: AWS Provider Configuration
provider "aws" {
  region = "eu-central-1" // Replace with your desired region
}
# // END: AWS Provider Configuration

// BEGIN: Create a simple subnet
resource "aws_default_subnet" "default" {
  availability_zone = "eu-central-1c"

  tags = {
    Name = "Default subnet for eu-central-1"
  }
}
// END: Create a simple subnet

// BEGIN: Create a simple security group
resource "aws_security_group" "simple_security_group" {
  name_prefix = "simple-security-group-"
  vpc_id      = aws_default_vpc.default.id

  ingress {
    protocol  = -1
    self      = true
    from_port = 0
    to_port   = 0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [aws_default_subnet.default.cidr_block]
  }
}
// END: Create a simple security group

// BEGIN: Create a simple vpc
resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}
// END: Create a simple vpc

// BEGIN: Create a simple role
resource "aws_iam_role" "simple_role" {
  name                = "simple_role"
  path                = "/"
  assume_role_policy  = data.aws_iam_policy_document.simple_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"]
}

data "aws_iam_policy_document" "simple_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}
// END: Create a simple role

// BEGIN: Create a SageMaker Domain
resource "aws_sagemaker_domain" "basic_domain" {
  domain_name = "basic-domain"
  auth_mode   = "IAM"
  vpc_id      = aws_default_vpc.default.id
  subnet_ids  = [aws_default_subnet.default.id] // Use default subnet ids

  default_user_settings {
    execution_role = aws_iam_role.simple_role.arn
  }

  default_space_settings {
    execution_role = aws_iam_role.simple_role.arn
  }
}
// END: Create a SageMaker Domain


// BEGIN: Create a SageMaker UserProfile
resource "aws_sagemaker_user_profile" "basic_user_profile" {
  domain_id         = aws_sagemaker_domain.basic_domain.id
  user_profile_name = "basic-user-profile"
  user_settings {
    execution_role = aws_iam_role.simple_role.arn
  }
}
// END: Create a SageMaker UserProfile

// BEGIN: Create a SageMaker UserProfile with JupyterLabs settings
resource "aws_sagemaker_user_profile" "large_user_profile" {
  domain_id         = aws_sagemaker_domain.basic_domain.id
  user_profile_name = "simple-user-profile"
  user_settings {
    execution_role = aws_iam_role.simple_role.arn
  }
}
// END: Create a SageMaker UserProfile

locals {
  users = [
    { name = "demo0", role = "${aws_iam_role.simple_role.arn}" },
    { name = "demo1", role = "${aws_iam_role.simple_role.arn}" },
    { name = "demo2", role = "${aws_iam_role.simple_role.arn}" },
  ]
}

// BEGIN: Create a SageMaker UserProfile with JupyterLabs settings
resource "aws_sagemaker_user_profile" "user_profile" {
  domain_id         = aws_sagemaker_domain.basic_domain.id
  for_each          = { for user_profile in local.users : "${user_profile.name}" => user_profile }
  user_profile_name = "${each.value.name}-user-profile"
  user_settings {
    execution_role = each.value.role
  }
}
// END: Create a SageMaker UserProfile

// BEGIN: Create a SageMaker Space
resource "aws_sagemaker_space" "test_space" {
  domain_id  = aws_sagemaker_domain.basic_domain.id
  space_name = "simple-space"
  ownership_settings {
    owner_user_profile_name = aws_sagemaker_user_profile.large_user_profile.user_profile_name
  }

  space_settings {
    app_type = "JupyterLab"
  }

  space_sharing_settings {
    sharing_type = "Private"
  }
}
// END: Create a SageMaker Space

# // BEGIN: Create a SageMaker App
resource "aws_sagemaker_app" "test_app" {
  domain_id = aws_sagemaker_domain.basic_domain.id
  #user_profile_name = aws_sagemaker_user_profile.large_user_profile.user_profile_name
  space_name = aws_sagemaker_space.test_space.space_name
  app_name   = "default"
  app_type   = "JupyterLab"
  resource_spec {
    instance_type       = "ml.t3.large"
    sagemaker_image_arn = "arn:aws:sagemaker:eu-central-1:545423591354:image/sagemaker-distribution-cpu"
  }
}
# // END: Create a SageMaker App

# // Begin: Create a SageMaker Notebook Instance
# resource "aws_sagemaker_notebook_instance" "test_notebook_instance" {
#   name            = "test-notebook-instance-three"
#   instance_type   = "ml.t3.medium"
#   role_arn        = aws_iam_role.simple_role.arn
#   subnet_id       = aws_default_subnet.default.id
#   security_groups = [aws_security_group.simple_security_group.id]
#   tags = {
#     Name = "Test Notebook Instance"
#   }
# }
# // End: Create a SageMaker Notebook Instance

// BEGIN: Create the IAM Role for the Lambda Function
resource "aws_iam_role" "simple_lambda_role" {
  name = "simple_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.simple_lambda_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"]
}

data "aws_iam_policy_document" "simple_lambda_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
// END: Create the IAM Role for the Lambda Function

// BEGIN: Create a Lambda Function
resource "aws_lambda_function" "test_lambda" {
  function_name = "test-lambda"
  handler       = "exports.handler"
  runtime       = "nodejs14.x"
  role          = aws_iam_role.simple_role.arn
  filename      = "lambda_function_payload.zip"
  source_code_hash = filebase64sha256("lambda_function_payload.zip")
}
// END: Create a Lambda Function