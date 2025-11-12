# AI Platform Makefile

.PHONY: help install test build deploy clean

help:
	@echo "AI Platform - Available Commands:"
	@echo "  make install    - Install all dependencies"
	@echo "  make test       - Run all tests"
	@echo "  make build      - Build all components"
	@echo "  make deploy     - Deploy to Kubernetes"
	@echo "  make simulate   - Run simulation tests"
	@echo "  make clean      - Clean build artifacts"

install:
	npm install
	pip install -r requirements.txt
	go mod download

test:
	npm test
	pytest tests/
	go test ./...

build:
	docker-compose build
	npm run build
	go build -o bin/ ./...

deploy:
	kubectl apply -f deployments/namespace.yaml
	kubectl apply -f deployments/
	helm upgrade --install ai-platform ./charts/ai-platform

simulate:
	npm run simulate:functional
	npm run simulate:load
	npm run simulate:chaos

clean:
	rm -rf node_modules/
	rm -rf dist/
	rm -rf bin/
	docker-compose down -v
