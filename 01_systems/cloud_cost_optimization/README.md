# Cloud Cost Optimization Platform

ML-driven cloud resource optimization and cost management

## Features

- Real-time cost monitoring
- Predictive cost analytics
- Resource rightsizing recommendations
- Multi-cloud support (AWS, Azure, GCP)

## Installation

```bash
npm install
```

## Configuration

Copy `.env.example` to `.env` and configure your environment variables:

```bash
cp .env.example .env
```

## Usage

### Development

```bash
npm run dev
```

### Production

```bash
npm start
```

### Testing

```bash
npm test
```

## API Endpoints

### Health Check
```
GET /health
```

### Get Status
```
GET /api/v1/status
```

### Process Request
```
POST /api/v1/process
Content-Type: application/json

{
  "data": "your_data_here"
}
```

## Docker

Build and run with Docker:

```bash
docker build -t cloud_cost_optimization .
docker run -p 3000:3000 cloud_cost_optimization
```

## License

Apache-2.0
