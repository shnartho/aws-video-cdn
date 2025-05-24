# Project-specific Instructions

This is a production-level video hosting service built with FastAPI, AWS S3, and CloudFront CDN.

## Core Components

- FastAPI application for video upload and serving endpoints
- AWS S3 for video storage
- CloudFront CDN for video delivery
- Pulumi for infrastructure as code
- Poetry for dependency management

## Code Style

- Follow PEP 8 standards
- Use type hints consistently
- Write comprehensive docstrings
- Use black for formatting with 88 character line length
- Use isort for import sorting

## Project Structure

- `app/` contains FastAPI application code
- `infrastructure/` contains Pulumi IaC code
- `tests/` contains test suite

## Key Functionality

- Video upload endpoint with metadata support
- Video serving via CloudFront CDN
- Proper error handling and validation
- Infrastructure as Code with Pulumi
