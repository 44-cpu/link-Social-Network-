from pydantic import BaseModel, ConfigDict

# ----------------- Blog Schemas -----------------
class BlogBase(BaseModel):
    title: str
    content: str
    image_url: str | None = None  # Optional field for S3 image URL

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int

    model_config = ConfigDict(from_attributes=True)  # orm_mode replacement

# ----------------- Career Schemas -----------------
class CareerBase(BaseModel):
    name: str
    email: str
    position: str

class CareerCreate(CareerBase):
    pass

class Career(CareerBase):
    id: int
    resume_url: str | None = None

    model_config = ConfigDict(from_attributes=True)  # orm_mode replacement
