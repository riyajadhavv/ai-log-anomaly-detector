variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  default     = "cloud-automation"
}

variable "environment" {
  description = "Deployment environment (dev/staging/prod)"
  default     = "dev"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "Amazon Machine Image ID"
  default     = "ami-0f58b397bc5c1f2e8"
}

variable "key_name" {
  description = "EC2 Key Pair name for SSH access"
}
