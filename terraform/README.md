## Infrastructure

Terraform for the bookings API: a VPC with two public subnets, a Postgres instance, the S3
bucket the nightly reconciliation exports are written to, and the IAM roles used by the
running service and by the deploy workflow.

State lives in the `peek-bookings-tfstate` bucket, configured in `providers.tf`.

### Usage

```bash
terraform init
terraform plan
terraform apply
```

If you do not have credentials for the state bucket, you can still check the configuration:

```bash
terraform init -backend=false
terraform validate
```

### Files

```
providers.tf   Provider, version constraints and remote state
variables.tf   Input variables
network.tf     VPC, subnets, routing and security groups
rds.tf         Postgres instance and subnet group
s3.tf          Exports bucket
iam.tf         Service role, GitHub OIDC provider and deploy role
outputs.tf     Endpoints and ARNs consumed by the deploy workflow
```
