
variable "aws_region" {
  description = "The AWS region where resources will be created."
  type        = string
  default     = "ap-southeast-1" # Updated to your preferred region
}

variable "bucket_name_prefix" {
  description = "A prefix for the S3 bucket name to help identify it."
  type        = string
  default     = "churn-mlops-artifacts"
}
