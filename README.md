# AWS Video CDN

A production-level video hosting service built with FastAPI, AWS S3, and CloudFront CDN.

## Features

- Video upload endpoint
- Video streaming via CloudFront CDN
- Infrastructure as Code with Pulumi
- Dependency management with Poetry

## Project Structure

```
aws-video-cdn/
├── app/                       # Application code
│   ├── api/                   # API endpoints
│   │   ├── endpoints/         # API endpoint modules
│   │   │   └── videos.py      # Video-related endpoints
│   │   └── routes.py          # API routes configuration
│   ├── core/                  # Core application code
│   │   ├── aws.py             # AWS integration (S3 client)
│   │   └── config.py          # Application settings
│   ├── schemas/               # Pydantic models/schemas
│   │   └── video.py           # Video-related schemas
│   └── main.py                # FastAPI application setup
├── infrastructure/            # Pulumi IaC code
│   └── __main__.py            # Pulumi program for AWS resources
├── tests/                     # Test suite
├── .env.example               # Environment variables example
├── Pulumi.yaml                # Pulumi project configuration
├── Pulumi.dev.yaml            # Development environment config
├── Pulumi.prod.yaml           # Production environment config
├── pyproject.toml             # Project dependencies (Poetry)
└── run.py                     # Application entry point
```

## Prerequisites

- Python 3.10+
- Poetry
- AWS account with appropriate permissions
- Pulumi account (free tier available)

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   poetry install
   ```
3. Copy `.env.example` to `.env` and update values:
   ```
   cp .env.example .env
   ```
4. Configure AWS credentials:
   ```
   aws configure
   ```
5. Deploy infrastructure:
   ```
   cd infrastructure
   pulumi up
   ```
6. Update `.env` with deployed resource information
7. Run the application:
   ```
   poetry run python run.py
   ```

## API Endpoints

### Upload Video
`POST /api/v1/videos/upload`

Upload a video file with optional metadata.

### Get Video
`GET /api/v1/videos/{video_id}`

Retrieve and stream a video by its ID.

### Get Video Info
`GET /api/v1/videos/{video_id}/info`

Get video metadata by ID.

## Troubleshooting

### Access Denied Errors
If you encounter "Access Denied" errors when accessing videos:

1. **Check S3 Permissions**: Ensure your S3 bucket policy allows CloudFront to access objects.
2. **Verify CloudFront Configuration**: Make sure your distribution has the correct origin and behaviors.
3. **Check Object ACL**: Videos should have public-read permissions.
4. **Path Issues**: Confirm you're using the correct path prefix (`videos/`) in your URLs.
5. **CloudFront Cache**: It might take up to 24 hours for permission changes to propagate. Try invalidating the CloudFront cache.

### How to use with Postman
1. **Upload Video**:
   - POST to `/api/v1/videos/upload`
   - Use form-data with a file field named `file`
   - Select your video file
   - Optionally add `title` and `description` fields

2. **Retrieve Video**:
   - Use the `id` returned from upload
   - GET `/api/v1/videos/{video_id}`

## Deployment

### Development
```
pulumi up --stack dev
```

### Production
```
pulumi up --stack prod
```

## License

MIT
