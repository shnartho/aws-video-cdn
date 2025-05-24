"""
Tests for video endpoints
"""
import io
import pytest
from unittest.mock import patch, MagicMock


def test_upload_video(client, mock_s3_client):
    """Test uploading a video"""
    # Create a test file
    test_file = io.BytesIO(b"test video content")
    
    # Send test request
    response = client.post(
        "/api/v1/videos/upload",
        files={"file": ("test_video.mp4", test_file, "video/mp4")},
        data={"title": "Test Video", "description": "Test Description"}
    )
    
    # Assert response
    assert response.status_code == 201
    assert "id" in response.json()
    assert "url" in response.json()
    assert response.json()["title"] == "Test Video"
    assert response.json()["description"] == "Test Description"
    
    # Assert S3 upload was called
    mock_s3_client["upload_video"].assert_called_once()


def test_upload_non_video_file(client, mock_s3_client):
    """Test uploading a non-video file"""
    # Create a test file
    test_file = io.BytesIO(b"test text content")
    
    # Send test request
    response = client.post(
        "/api/v1/videos/upload",
        files={"file": ("test.txt", test_file, "text/plain")},
    )
    
    # Assert response
    assert response.status_code == 400
    assert "File must be a video" in response.json()["detail"]
    
    # Assert S3 upload was not called
    mock_s3_client["upload_video"].assert_not_called()


def test_get_video(client, mock_s3_client):
    """Test getting a video"""
    # Set up the mock
    video_id = "test-id"
    mock_s3_client["get_video_url"].return_value = f"https://test-cdn.example.com/videos/{video_id}.mp4"
    
    # Send test request
    response = client.get(f"/api/v1/videos/{video_id}", allow_redirects=False)
    
    # Assert redirect response
    assert response.status_code == 307
    assert response.headers["location"] == f"https://test-cdn.example.com/videos/{video_id}.mp4"
    
    # Assert get_video_url was called
    mock_s3_client["get_video_url"].assert_called_once()


def test_get_video_info(client, mock_s3_client):
    """Test getting video info"""
    # Set up the mock
    video_id = "test-id"
    mock_s3_client["get_video_url"].return_value = f"https://test-cdn.example.com/videos/{video_id}.mp4"
    
    # Send test request
    response = client.get(f"/api/v1/videos/{video_id}/info")
    
    # Assert response
    assert response.status_code == 200
    assert response.json()["id"] == video_id
    assert "url" in response.json()
    assert "title" in response.json()
    assert "description" in response.json()
    
    # Assert get_video_url was called
    mock_s3_client["get_video_url"].assert_called_once()
