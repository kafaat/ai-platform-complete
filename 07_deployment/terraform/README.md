# Terraform Infrastructure

This directory contains Terraform configuration for deploying the AI Platform infrastructure on AWS.

## Prerequisites

- Terraform >= 1.0
- AWS CLI configured
- kubectl installed

## Quick Start

1. Copy the example variables file:
```bash
cp terraform.tfvars.example terraform.tfvars
```

2. Edit `terraform.tfvars` and set your values, especially:
   - `db_password`
   - `aws_region` (if different from us-east-1)

3. Initialize Terraform:
```bash
terraform init
```

4. Plan the deployment:
```bash
terraform plan
```

5. Apply the configuration:
```bash
terraform apply
```

## Resources Created

- **VPC**: Multi-AZ VPC with public and private subnets
- **EKS Cluster**: Kubernetes cluster with auto-scaling node groups
- **RDS PostgreSQL**: Multi-AZ database with automated backups
- **ElastiCache Redis**: Multi-AZ Redis cluster
- **Security Groups**: Properly configured security groups
- **IAM Roles**: Required IAM roles and policies

## Outputs

After applying, you'll get:
- EKS cluster endpoint
- RDS endpoint
- Redis endpoint
- VPC and subnet IDs

## Connecting to the Cluster

```bash
aws eks update-kubeconfig --region us-east-1 --name ai-platform-cluster
kubectl get nodes
```

## Cleanup

To destroy all resources:
```bash
terraform destroy
```

**Warning**: This will delete all resources including databases. Make sure you have backups!

## Cost Estimation

Approximate monthly costs (us-east-1):
- EKS Cluster: $73
- EC2 Instances (10 x t3.xlarge): ~$1,200
- RDS (db.r6g.xlarge): ~$350
- ElastiCache (3 x cache.r6g.large): ~$450
- NAT Gateways: ~$100
- **Total**: ~$2,173/month

Costs may vary based on usage and data transfer.
