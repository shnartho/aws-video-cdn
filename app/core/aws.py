import boto3
from botocore.exceptions import ClientError
import logging
from typing import Optional, BinaryIO, Dict, Any

from app.core.config import settings

logger = logging.getLogger(__name__)


class S3Client:
    """Client for interacting with AWS S3"""
    
    def __init__(self, region_name: str = settings.AWS_REGION):
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.bucket_name = settings.S3_BUCKET_NAME
        self.cloudfront_domain = settings.CLOUDFRONT_DOMAIN
    
    def upload_video(self, file_obj: BinaryIO, file_name: str, metadata: Optional[Dict[str, str]] = None) -> str:
        """
        Upload a video file to S3 bucket
        
        Args:
            file_obj: File-like object to upload
            file_name: Name of the file in S3
            metadata: Optional metadata for the S3 object
            
        Returns:
            S3 object URL or CloudFront URL if configured
        """
        try:
            extra_args = {
                'ContentType': 'video/mp4',  # Assuming MP4 format, adjust as needed
                'ACL': 'public-read',  # Make objects publicly readable so CloudFront can access them
            }
            
            if metadata:
                extra_args['Metadata'] = metadata
                
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                file_name,
                ExtraArgs=extra_args
            )
            
            logger.info(f"Successfully uploaded video {file_name} to S3 bucket {self.bucket_name}")
            
            # Return CloudFront URL if configured, otherwise return S3 URL
            if self.cloudfront_domain:
                return f"https://{self.cloudfront_domain}/{file_name}"
            else:
                return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
                
        except ClientError as e:
            logger.error(f"Error uploading video to S3: {str(e)}")
            raise
    
    def get_video_url(self, file_name: str) -> str:
        """
        Get the URL for a video file
        
        Args:
            file_name: Name of the file in S3
            
        Returns:
            CloudFront URL if configured, otherwise S3 URL
        """
        # Check if file exists
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise ValueError(f"Video file {file_name} does not exist in bucket")
            else:
                logger.error(f"Error checking video existence: {str(e)}")
                raise
                
        # Return CloudFront URL if configured, otherwise return S3 URL
        if self.cloudfront_domain:
            return f"https://{self.cloudfront_domain}/{file_name}"
        else:
            return f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
            
    def delete_video(self, file_name: str) -> None:
        """
        Delete a video file from S3
        
        Args:
            file_name: Name of the file to delete
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            logger.info(f"Successfully deleted video {file_name} from S3 bucket {self.bucket_name}")
        except ClientError as e:
            logger.error(f"Error deleting video from S3: {str(e)}")
            raise
