
provider "aws" {
  region = var.aws_region
}

# Create a random suffix to ensure the S3 bucket name is globally unique.
resource "random_pet" "bucket_name_suffix" {
  length = 2
}

# Create the S3 bucket for MLflow artifacts.
resource "aws_s3_bucket" "mlflow_artifacts" {
  bucket = "${var.bucket_name_prefix}-${random_pet.bucket_name_suffix.id}"

  tags = {
    Name      = "MLflow Artifact Store"
    Project   = "Customer Churn MLOps"
    ManagedBy = "Terraform"
  }
}

# Create a dedicated IAM user for the MLflow application.
resource "aws_iam_user" "mlflow_user" {
  name = "mlflow-s3-user-${random_pet.bucket_name_suffix.id}"
}

# Define the custom, least-privilege IAM policy in-line.
# This policy references the S3 bucket created above.
resource "aws_iam_policy" "mlflow_policy" {
  name        = "mlflow-s3-policy-${random_pet.bucket_name_suffix.id}"
  description = "Allows read/write access to a specific MLflow S3 bucket."

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "AllowListBucket",
        Effect = "Allow",
        Action = [
          "s3:ListBucket"
        ],
        Resource = [
          aws_s3_bucket.mlflow_artifacts.arn # Reference the bucket directly
        ]
      },
      {
        Sid    = "AllowReadWriteDeleteObjects",
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Resource = [
          "${aws_s3_bucket.mlflow_artifacts.arn}/*" # Reference objects inside the bucket
        ]
      }
    ]
  })
}

# Attach the policy to the user.
resource "aws_iam_user_policy_attachment" "mlflow_attachment" {
  user       = aws_iam_user.mlflow_user.name
  policy_arn = aws_iam_policy.mlflow_policy.arn
}

# Create an access key for the new IAM user.
resource "aws_iam_access_key" "mlflow_key" {
  user = aws_iam_user.mlflow_user.name
}

# Output the bucket name and the new user's credentials.
output "mlflow_bucket_name" {
  value = aws_s3_bucket.mlflow_artifacts.bucket
}

output "mlflow_user_access_key_id" {
  value     = aws_iam_access_key.mlflow_key.id
  sensitive = true
}

output "mlflow_user_secret_access_key" {
  value     = aws_iam_access_key.mlflow_key.secret
  sensitive = true
}
