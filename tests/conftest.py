"""
Conftest for pytest
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.core.aws import S3Client


@pytest.fixture
def client():
    """
    Create a test client for FastAPI application
    """
    return TestClient(app)


@pytest.fixture
def mock_s3_client():
    """
    Create a mocked S3 client for testing
    """
    with patch.object(S3Client, '__init__', return_value=None) as mock_init:
        with patch.object(S3Client, 'upload_video') as mock_upload:
            with patch.object(S3Client, 'get_video_url') as mock_get_url:
                mock_upload.return_value = "https://test-cdn.example.com/videos/test-id.mp4"
                mock_get_url.return_value = "https://test-cdn.example.com/videos/test-id.mp4"
                
                yield {
                    "init": mock_init,
                    "upload_video": mock_upload,
                    "get_video_url": mock_get_url
                }
