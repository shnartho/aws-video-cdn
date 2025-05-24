"""
Pulumi program to create AWS S3 bucket and CloudFront distribution for video hosting
"""

import pulumi
import pulumi_aws as aws
from pulumi_aws import s3, cloudfront

# Import configuration
config = pulumi.Config()
s3_bucket_name = config.get("s3_bucket_name") or "video-storage-bucket"
environment = config.get("environment") or "dev"

# Fully qualified bucket name with environment
bucket_name = f"{s3_bucket_name}-{environment}-{pulumi.get_stack()}"

# Create an S3 bucket for storing videos
video_bucket = s3.Bucket(
    "video-bucket",
    bucket=bucket_name,
    acl="private",    cors_rules=[{
        "allowedMethods": ["GET"],
        "allowedOrigins": ["*"],  # In production, restrict to your domains
        "allowedHeaders": ["*"],
        "maxAgeSeconds": 3000
    }],
    # Enable website hosting to allow direct S3 URL access
    website={
        "indexDocument": "index.html",
        "errorDocument": "error.html"
    },
    # Add lifecycle rules for managing objects
    lifecycle_rules=[{
        "enabled": True,
        "id": "cleanup-old-videos",
        "prefix": "videos/",
        "tags": {
            "archived": "true"
        },
        "expiration": {
            "days": 365  # Old videos marked as archived will be deleted after 1 year
        }
    }],
    tags={
        "Name": bucket_name,
        "Environment": environment,
        "ManagedBy": "Pulumi",
    }
)

# Create an Origin Access Identity for CloudFront
origin_access_identity = cloudfront.OriginAccessIdentity(
    "video-oai",
    comment=f"OAI for {bucket_name}"
)

# Configure public access block settings to allow public policies
public_access_block = s3.BucketPublicAccessBlock(
    "video-bucket-public-access",
    bucket=video_bucket.id,
    block_public_acls=False,
    block_public_policy=False,
    ignore_public_acls=False,
    restrict_public_buckets=False
)

# Create a bucket policy that allows CloudFront to access the bucket
bucket_policy = s3.BucketPolicy(
    "video-bucket-policy",
    bucket=video_bucket.id,
    # Add dependency to ensure the public access block is configured before policy
    opts=pulumi.ResourceOptions(depends_on=[public_access_block]),policy=pulumi.Output.all(
        video_bucket.id, 
        origin_access_identity.id
    ).apply(
        lambda args: f'''{{
            "Version": "2012-10-17",
            "Statement": [
                {{
                    "Effect": "Allow",
                    "Principal": {{
                        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {args[1]}"
                    }},
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::{args[0]}/*"
                }},
                {{
                    "Effect": "Allow",
                    "Principal": {{"AWS": "*"}},
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::{args[0]}/videos/*"
                }}
            ]
        }}'''
    )
)

# Create CloudFront distribution
cdn = cloudfront.Distribution(
    "video-cdn",
    enabled=True,
    is_ipv6_enabled=True,
    comment=f"Distribution for {bucket_name}",
    default_root_object="index.html",
    
    # Origins
    origins=[{
        "originId": video_bucket.arn,
        "domainName": video_bucket.bucket_regional_domain_name,
        "s3_origin_config": {
            "originAccessIdentity": origin_access_identity.cloudfront_access_identity_path
        },
    }],
    
    # Default cache behavior
    default_cache_behavior={
        "allowedMethods": ["GET", "HEAD", "OPTIONS"],
        "cachedMethods": ["GET", "HEAD"],
        "targetOriginId": video_bucket.arn,
        "forwardedValues": {
            "queryString": False,
            "cookies": {
                "forward": "none"
            },
        },
        "viewerProtocolPolicy": "redirect-to-https",
        "minTtl": 0,
        "defaultTtl": 3600,
        "maxTtl": 86400,
        "compress": True,
    },
    
    # Additional cache behaviors for video files
    ordered_cache_behaviors=[{
        "pathPattern": "videos/*",
        "allowedMethods": ["GET", "HEAD", "OPTIONS"],
        "cachedMethods": ["GET", "HEAD"],
        "targetOriginId": video_bucket.arn,
        "forwardedValues": {
            "queryString": False,
            "cookies": {
                "forward": "none"
            },
        },
        "viewerProtocolPolicy": "redirect-to-https",
        "minTtl": 0,
        "defaultTtl": 86400,  # 1 day cache for videos
        "maxTtl": 604800,     # 7 days max cache 
        "compress": True,
    }],
    
    # Price class
    price_class="PriceClass_100",  # Use only US and Europe locations (cheapest option)
    
    # Restrictions
    restrictions={
        "geoRestriction": {
            "restrictionType": "none",
        },
    },
    
    # SSL Certificate
    viewer_certificate={
        "cloudfront_default_certificate": True,
    },
    
    # Tags
    tags={
        "Name": f"{bucket_name}-cdn",
        "Environment": environment,
        "ManagedBy": "Pulumi",
    }
)

# Export the bucket name, S3 website URL, and CDN domain
pulumi.export("bucket_name", video_bucket.id)
pulumi.export("s3_website_endpoint", video_bucket.website_endpoint)
pulumi.export("s3_domain", video_bucket.bucket_regional_domain_name)
pulumi.export("cdn_domain", cdn.domain_name)
