# API Reference

## Authentication

All API requests require authentication using JWT tokens.

### Get Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password"
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": "7d"
}
```

### Use Token

Include the token in the Authorization header:

```http
Authorization: Bearer <token>
```

## Common Endpoints

All services expose these common endpoints:

### Health Check

```http
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "service-name",
  "version": "1.0.0",
  "timestamp": "2025-11-12T07:00:00Z"
}
```

### Service Status

```http
GET /api/v1/status
```

Response:
```json
{
  "service": "service-name",
  "status": "running",
  "timestamp": "2025-11-12T07:00:00Z"
}
```

## Service-Specific APIs

### DevOps Automation

#### Create Pipeline

```http
POST /api/v1/pipelines
Content-Type: application/json

{
  "name": "my-pipeline",
  "repository": "https://github.com/org/repo",
  "branch": "main",
  "stages": ["build", "test", "deploy"]
}
```

#### Get Pipeline Status

```http
GET /api/v1/pipelines/{id}/status
```

### Documentation Automation

#### Generate Documentation

```http
POST /api/v1/docs/generate
Content-Type: application/json

{
  "repository": "https://github.com/org/repo",
  "branch": "main",
  "format": "markdown"
}
```

### Cloud Cost Optimization

#### Get Cost Analysis

```http
GET /api/v1/costs/analysis?period=30d
```

#### Get Recommendations

```http
GET /api/v1/costs/recommendations
```

### AI Code Review

#### Submit Code for Review

```http
POST /api/v1/review
Content-Type: application/json

{
  "repository": "https://github.com/org/repo",
  "pullRequest": 123
}
```

### Data Pipeline Orchestration

#### Create Workflow

```http
POST /api/v1/workflows
Content-Type: application/json

{
  "name": "data-processing",
  "tasks": [
    {
      "id": "extract",
      "type": "extract",
      "config": {}
    },
    {
      "id": "transform",
      "type": "transform",
      "dependsOn": ["extract"]
    }
  ]
}
```

### Customer Experience

#### Get Recommendations

```http
GET /api/v1/recommendations?userId=123
```

### Security Operations Center

#### Get Security Alerts

```http
GET /api/v1/security/alerts?severity=high
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2025-11-12T07:00:00Z"
}
```

### Common Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Rate Limiting

- Rate limit: 1000 requests per hour per API key
- Rate limit headers included in all responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Webhooks

Services can send webhooks for events:

### Configure Webhook

```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "url": "https://your-server.com/webhook",
  "events": ["pipeline.completed", "alert.created"],
  "secret": "your-webhook-secret"
}
```

### Webhook Payload

```json
{
  "event": "pipeline.completed",
  "timestamp": "2025-11-12T07:00:00Z",
  "data": {
    "pipelineId": "123",
    "status": "success"
  }
}
```
