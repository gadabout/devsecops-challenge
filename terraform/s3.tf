resource "aws_s3_bucket" "exports" {
  bucket = "peek-bookings-exports-${var.environment}"
}

# Finance pulls the nightly reconciliation CSV straight from the bucket URL.
resource "aws_s3_bucket_ownership_controls" "exports" {
  bucket = aws_s3_bucket.exports.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "exports" {
  depends_on = [aws_s3_bucket_ownership_controls.exports]

  bucket = aws_s3_bucket.exports.id
  acl    = "public-read"
}
