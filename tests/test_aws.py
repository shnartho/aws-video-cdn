"""
Tests for core AWS functionality
"""
import pytest
from unittest.mock import patch, MagicMock
import botocore.exceptions
import io

from app.core.aws import S3Client


class TestS3Client:
    """Tests for S3Client"""
    
    @patch('boto3.client')
    def test_upload_video(self, mock_boto_client):
        """Test uploading a video to S3"""
        # Setup mock
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        # Create test client
        s3_client = S3Client()
        s3_client.s3_client = mock_s3
        s3_client.bucket_name = "test-bucket"
        s3_client.cloudfront_domain = "test-cdn.example.com"
        
        # Test file
        test_file = io.BytesIO(b"test video content")
        file_name = "videos/test-id.mp4"
        
        # Call upload_video
        result = s3_client.upload_video(test_file, file_name)
        
        # Assert upload was called
        mock_s3.upload_fileobj.assert_called_once_with(
            test_file,
            "test-bucket",
            file_name,
            ExtraArgs={'ContentType': 'video/mp4'}
        )
        
        # Assert result is CloudFront URL
        assert result == f"https://test-cdn.example.com/{file_name}"
    
    @patch('boto3.client')
    def test_upload_video_without_cloudfront(self, mock_boto_client):
        """Test uploading a video to S3 without CloudFront"""
        # Setup mock
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        # Create test client
        s3_client = S3Client()
        s3_client.s3_client = mock_s3
        s3_client.bucket_name = "test-bucket"
        s3_client.cloudfront_domain = None
        
        # Test file
        test_file = io.BytesIO(b"test video content")
        file_name = "videos/test-id.mp4"
        
        # Call upload_video
        result = s3_client.upload_video(test_file, file_name)
        
        # Assert result is S3 URL
        assert result == f"https://test-bucket.s3.amazonaws.com/{file_name}"
    
    @patch('boto3.client')
    def test_get_video_url(self, mock_boto_client):
        """Test getting a video URL"""
        # Setup mock
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        # Create test client
        s3_client = S3Client()
        s3_client.s3_client = mock_s3
        s3_client.bucket_name = "test-bucket"
        s3_client.cloudfront_domain = "test-cdn.example.com"
        
        file_name = "videos/test-id.mp4"
        
        # Call get_video_url
        result = s3_client.get_video_url(file_name)
        
        # Assert head_object was called
        mock_s3.head_object.assert_called_once_with(
            Bucket="test-bucket",
            Key=file_name
        )
        
        # Assert result is CloudFront URL
        assert result == f"https://test-cdn.example.com/{file_name}"
    
    @patch('boto3.client')
    def test_get_video_url_not_found(self, mock_boto_client):
        """Test getting a video URL for a non-existent file"""
        # Setup mock
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3
        
        # Mock head_object to raise 404
        error_response = {"Error": {"Code": "404"}}
        mock_s3.head_object.side_effect = botocore.exceptions.ClientError(
            error_response, "HeadObject"
        )
        
        # Create test client
        s3_client = S3Client()
        s3_client.s3_client = mock_s3
        s3_client.bucket_name = "test-bucket"
        
        file_name = "videos/non-existent.mp4"
        
        # Call get_video_url and expect exception
        with pytest.raises(ValueError, match="Video file .* does not exist"):
            s3_client.get_video_url(file_name)
