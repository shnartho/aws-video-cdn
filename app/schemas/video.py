from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class VideoBase(BaseModel):
    """Base video schema"""
    title: Optional[str] = None
    description: Optional[str] = None


class VideoUpload(VideoBase):
    """Schema for video upload request"""
    pass


class VideoResponse(VideoBase):
    """Schema for video upload response"""
    id: str
    filename: str
    url: str
    title: str
    description: str = ""


class VideoMetadata(VideoBase):
    """Schema for video metadata"""
    id: str
    url: str
    title: str
    description: str = ""
