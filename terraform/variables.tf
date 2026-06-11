variable "region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name, used in resource names and tags."
  type        = string
  default     = "production"
}

variable "db_username" {
  description = "Master username for the bookings database."
  type        = string
  default     = "peek"
}

variable "db_password" {
  description = "Master password for the bookings database."
  type        = string
  default     = "hunter2"
}

variable "db_instance_class" {
  description = "Instance class for the bookings database."
  type        = string
  default     = "db.t3.medium"
}

variable "github_org" {
  description = "GitHub organisation that runs the deploy workflow."
  type        = string
  default     = "gadabout"
}
