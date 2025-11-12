# Deployment Guide

## Prerequisites

- AWS account with appropriate permissions
- kubectl installed
- Terraform >= 1.0
- Docker installed
- Node.js >= 18

## Infrastructure Deployment

### 1. Terraform Setup

```bash
cd 07_deployment/terraform

# Copy and edit variables
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -out=tfplan

# Apply infrastructure
terraform apply tfplan
```

### 2. Configure kubectl

```bash
aws eks update-kubeconfig --region us-east-1 --name ai-platform-cluster
kubectl get nodes
```

## Application Deployment

### 1. Build Docker Images

```bash
# Build all services
for service in devops-automation documentation-automation cloud-cost-optimization ai-code-review data-pipeline-orchestration customer-experience security-operations-center; do
  docker build -t ai-platform/$service:1.0.0 01_systems/${service//-/_}/
done
```

### 2. Push to Registry

```bash
# Tag and push to ECR
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=us-east-1

for service in devops-automation documentation-automation cloud-cost-optimization ai-code-review data-pipeline-orchestration customer-experience security-operations-center; do
  docker tag ai-platform/$service:1.0.0 $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-platform/$service:1.0.0
  docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/ai-platform/$service:1.0.0
done
```

### 3. Deploy to Kubernetes

```bash
cd 07_deployment/kubernetes

# Create namespace
kubectl apply -f namespace.yaml

# Create secrets
kubectl apply -f secrets.yaml

# Create configmap
kubectl apply -f configmap.yaml

# Deploy infrastructure
kubectl apply -f postgres.yaml
kubectl apply -f redis.yaml

# Wait for infrastructure
kubectl wait --for=condition=ready pod -l app=postgres -n ai-platform --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n ai-platform --timeout=300s

# Deploy services
for service in devops-automation documentation-automation cloud-cost-optimization ai-code-review data-pipeline-orchestration customer-experience security-operations-center; do
  kubectl apply -f $service.yaml
done

# Deploy ingress
kubectl apply -f ingress.yaml
```

### 4. Verify Deployment

```bash
# Check all pods
kubectl get pods -n ai-platform

# Check services
kubectl get svc -n ai-platform

# Check ingress
kubectl get ingress -n ai-platform

# Check logs
kubectl logs -f deployment/devops-automation -n ai-platform
```

## Local Development Deployment

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Using Make

```bash
# Install dependencies
make install

# Build all components
make build

# Run tests
make test

# Start development environment
make dev
```

## Configuration

### Environment Variables

Each service requires the following environment variables:

```bash
# Server
PORT=3000
NODE_ENV=production

# Database
DB_HOST=postgres-service
DB_PORT=5432
DB_NAME=aiplatform
DB_USER=postgres
DB_PASSWORD=<secret>

# Redis
REDIS_HOST=redis-service
REDIS_PORT=6379

# AI Services
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
```

### Secrets Management

```bash
# Create secrets in Kubernetes
kubectl create secret generic platform-secrets   --from-literal=OPENAI_API_KEY=<your-key>   --from-literal=ANTHROPIC_API_KEY=<your-key>   --from-literal=DB_PASSWORD=<your-password>   -n ai-platform
```

## Monitoring Setup

### Prometheus

```bash
# Install Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

### Grafana

```bash
# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Default credentials: admin/prom-operator
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n ai-platform

# Check logs
kubectl logs <pod-name> -n ai-platform

# Check events
kubectl get events -n ai-platform --sort-by='.lastTimestamp'
```

### Database Connection Issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15-alpine --restart=Never -n ai-platform -- psql -h postgres-service -U postgres -d aiplatform
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints -n ai-platform

# Check ingress
kubectl describe ingress platform-ingress -n ai-platform

# Test service internally
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -n ai-platform -- curl http://devops-automation-service/health
```

## Rollback Procedures

### Kubernetes Rollback

```bash
# View rollout history
kubectl rollout history deployment/devops-automation -n ai-platform

# Rollback to previous version
kubectl rollout undo deployment/devops-automation -n ai-platform

# Rollback to specific revision
kubectl rollout undo deployment/devops-automation --to-revision=2 -n ai-platform
```

### Terraform Rollback

```bash
# View state
terraform show

# Rollback changes
terraform apply -auto-approve <previous-tfplan>
```

## Scaling

### Manual Scaling

```bash
# Scale deployment
kubectl scale deployment/devops-automation --replicas=5 -n ai-platform
```

### Auto-scaling

```bash
# Check HPA status
kubectl get hpa -n ai-platform

# Adjust HPA
kubectl edit hpa devops-automation-hpa -n ai-platform
```

## Backup & Restore

### Database Backup

```bash
# Create backup
kubectl exec -it postgres-0 -n ai-platform -- pg_dump -U postgres aiplatform > backup.sql

# Restore backup
kubectl exec -i postgres-0 -n ai-platform -- psql -U postgres aiplatform < backup.sql
```

### Configuration Backup

```bash
# Backup all configurations
kubectl get all,configmap,secret -n ai-platform -o yaml > backup.yaml
```

## Health Checks

### Service Health

```bash
# Check all service health endpoints
for service in devops-automation documentation-automation cloud-cost-optimization ai-code-review data-pipeline-orchestration customer-experience security-operations-center; do
  echo "Checking $service..."
  kubectl exec -it deployment/$service -n ai-platform -- curl localhost:3000/health
done
```

## Performance Tuning

### Resource Optimization

```bash
# View resource usage
kubectl top pods -n ai-platform
kubectl top nodes

# Adjust resource limits
kubectl edit deployment/devops-automation -n ai-platform
```

## Security Hardening

### Network Policies

```bash
# Apply network policies
kubectl apply -f network-policies.yaml -n ai-platform
```

### Pod Security

```bash
# Enable pod security standards
kubectl label namespace ai-platform pod-security.kubernetes.io/enforce=restricted
```
