from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

# ----------------- Blog Schemas -----------------
class BlogBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None  # Optional field for S3 image URL

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # orm_mode replacement

# ----------------- Career Schemas -----------------
class CareerBase(BaseModel):
    name: str
    email: EmailStr  # will validate email automatically
    position: str

class CareerCreate(CareerBase):
    """Used when creating a career application.
       resume_url will be filled after upload to S3."""
    resume_url: Optional[str] = None  # optional; added for S3 file URL

class Career(CareerBase):
    id: int
    resume_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)  # orm_mode replacement
