# Documentation Automation System

AI-powered documentation generation and maintenance

## Features

- Automatic API documentation generation
- Code-to-docs synchronization
- Multi-language support
- Version control integration

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
docker build -t documentation_automation .
docker run -p 3000:3000 documentation_automation
```

## License

Apache-2.0
