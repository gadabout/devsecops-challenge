# Role assumed by the running API tasks.
resource "aws_iam_role" "app" {
  name = "bookings-api-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy" "app" {
  name = "bookings-api"
  role = aws_iam_role.app.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

# Role assumed by the GitHub Actions deploy workflow, using OIDC rather than a
# long-lived access key.
resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

resource "aws_iam_role" "github_deploy" {
  name = "bookings-github-deploy-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRoleWithWebIdentity"
      Principal = { Federated = aws_iam_openid_connect_provider.github.arn }
      Condition = {
        StringLike = {
          "token.actions.githubusercontent.com:sub" = "repo:${var.github_org}/*"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "github_deploy" {
  name = "bookings-deploy"
  role = aws_iam_role.github_deploy.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ecr:GetAuthorizationToken", "ecr:PutImage", "ecr:UploadLayerPart"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["ecs:UpdateService", "ecs:DescribeServices"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "iam:PassRole"
        Resource = aws_iam_role.app.arn
      },
    ]
  })
}
