from pydantic import BaseModel, ConfigDict

class BlogBase(BaseModel):
    title: str
    content: str
    image_url: str | None = None  # Optional field for S3 image URL

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)  # orm_mode replacement
