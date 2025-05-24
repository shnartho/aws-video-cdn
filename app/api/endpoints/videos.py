from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Path, Query, BackgroundTasks
from fastapi.responses import RedirectResponse
import uuid
import logging
from typing import Any

from app.core.aws import S3Client
from app.schemas.video import VideoResponse, VideoMetadata

router = APIRouter()
logger = logging.getLogger(__name__)

# Dependency to get S3 client
def get_s3_client() -> S3Client:
    return S3Client()


@router.post("/upload", response_model=VideoResponse, status_code=201)
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: str = Query(None, description="Optional title for the video"),
    description: str = Query(None, description="Optional description for the video"),
    s3_client: S3Client = Depends(get_s3_client)
) -> Any:
    """
    Upload a video file to S3 and optionally serve via CloudFront CDN.
    
    Args:
        file: The video file to upload
        title: Optional title for the video
        description: Optional description for the video
        
    Returns:
        JSON with video ID and URL
    """
    if not file.content_type or not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")
        
    try:
        # Generate a unique ID for the video
        video_id = str(uuid.uuid4())
        
        # Extract file extension
        original_filename = file.filename or "video.mp4"
        file_extension = original_filename.split(".")[-1] if "." in original_filename else "mp4"
        
        # Create the S3 key (filename)
        s3_key = f"videos/{video_id}.{file_extension}"
        
        # Prepare metadata
        metadata = {
            "title": title or original_filename,
            "description": description or "",
            "original_filename": original_filename
        }
        
        # Upload the file to S3
        url = s3_client.upload_video(
            file_obj=file.file, 
            file_name=s3_key,
            metadata={k: v for k, v in metadata.items() if v}
        )
        
        return VideoResponse(
            id=video_id,
            filename=s3_key,
            url=url,
            title=metadata["title"],
            description=metadata["description"]
        )
            
    except Exception as e:
        logger.error(f"Error uploading video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading video: {str(e)}")


@router.get("/{video_id}", response_class=RedirectResponse, status_code=307)
async def get_video(
    video_id: str = Path(..., description="The ID of the video to retrieve"),
    s3_client: S3Client = Depends(get_s3_client)
) -> Any:
    """
    Get a video by ID and redirect to its URL
    
    Args:
        video_id: The ID of the video
        
    Returns:
        Redirect to the video URL (S3 or CloudFront)
    """
    try:
        # First, check if the video ID already contains the extension
        if not video_id.endswith(".mp4"):
            # Construct the S3 key assuming MP4 format
            s3_key = f"videos/{video_id}.mp4"
        else:
            # Use the video_id as is if it already has an extension
            s3_key = f"videos/{video_id}"
        
        # Get the video URL
        url = s3_client.get_video_url(s3_key)
        
        # Redirect to the URL
        return url
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving video: {str(e)}")


@router.get("/{video_id}/info", response_model=VideoMetadata)
async def get_video_info(
    video_id: str = Path(..., description="The ID of the video to get info for"),
    s3_client: S3Client = Depends(get_s3_client)
) -> Any:
    """
    Get video metadata by ID
    
    Args:
        video_id: The ID of the video
        
    Returns:
        Video metadata
    """
    try:
        # Construct the S3 key assuming MP4 format
        s3_key = f"videos/{video_id}.mp4"
        
        # Get the video URL
        url = s3_client.get_video_url(s3_key)
        
        # In a real app, you'd fetch metadata from a database
        # For this example, we'll just return basic info
        return VideoMetadata(
            id=video_id,
            url=url,
            title=f"Video {video_id}",
            description="Video description would be fetched from database"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving video info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving video info: {str(e)}")
