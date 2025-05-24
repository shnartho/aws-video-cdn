# AWS Video CDN

A production-level video hosting service built with FastAPI, AWS S3, and CloudFront CDN.

## API Endpoints

### Upload Video
`POST /api/v1/videos/upload`

Upload a video file with optional metadata.

#### Example Upload Response:

![Upload Response](docs/screenshots/upload.png)

### Get Video
`GET /api/v1/videos/{video_id}`

Retrieve and stream a video by its ID.

#### Example Get Video Response:

![Get Response](docs/screenshots/get.png)

### Get Video Info
`GET /api/v1/videos/{video_id}/info`

Get video metadata by ID.

## CloudFront CDN Integration

Our service uses AWS CloudFront as a Content Delivery Network to improve video delivery performance worldwide.

![CloudFront Dashboard](docs/screenshots/cloudfront.png)

![CloudFront Configuration](docs/screenshots/cloudfront00.png)

## Performance Comparison

Tests conducted between our AWS infrastructure in Ireland and a client in Australia show that using CloudFront CDN provides significantly better performance compared to direct S3 access:

### S3 Direct Access Speed:

![S3 Speed Test](docs/screenshots/s3speed.png)

### CloudFront CDN Speed (2x faster):

![CloudFront Speed Test](docs/screenshots/cfspeed.png)

CloudFront significantly improves performance over S3, as shown by lower total, resolve, connection, and download times. In Auckland, CloudFront's total time was 2437 ms (32 ms resolve, 127 ms connection, 2278 ms download) compared to S3's 4516 ms (63 ms resolve, 280 ms connection, 4173 ms download). Similarly, for Sydney, CloudFront achieved 2490 ms total (9 ms resolve, 155 ms connection, 2326 ms download), which is much faster than S3's 5319 ms total (23 ms resolve, 327 ms connection, 4969 ms download). The data clearly demonstrates CloudFront's efficacy in reducing all aspects of content delivery latency.

## License

MIT
