output "database_endpoint" {
  description = "Hostname and port of the bookings database."
  value       = aws_db_instance.bookings.endpoint
}

output "exports_bucket" {
  description = "Bucket holding the nightly reconciliation exports."
  value       = aws_s3_bucket.exports.bucket
}

output "app_role_arn" {
  description = "Role assumed by the API tasks."
  value       = aws_iam_role.app.arn
}

output "deploy_role_arn" {
  description = "Role assumed by the GitHub Actions deploy workflow."
  value       = aws_iam_role.github_deploy.arn
}
