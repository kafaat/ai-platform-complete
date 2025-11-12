# AI Code Review System

Automated code quality and security analysis

## Features

- Automated code quality checks
- Security vulnerability detection
- Best practices enforcement
- AI-powered suggestions

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
docker build -t ai_code_review .
docker run -p 3000:3000 ai_code_review
```

## License

Apache-2.0
