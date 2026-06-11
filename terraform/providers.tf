terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "peek-bookings-tfstate"
    key    = "bookings/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Service     = "bookings-api"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
