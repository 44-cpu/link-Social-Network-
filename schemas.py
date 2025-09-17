from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

# ----------------- Blog Schemas -----------------
class BlogBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ----------------- Career Schemas -----------------
class CareerBase(BaseModel):
    name: str
    email: EmailStr
    position: str
    type: str = "external"  # default; actual default DB se uthega

class CareerCreate(CareerBase):
    """Used when creating a career application."""
    resume_url: Optional[str] = None

class Career(CareerBase):
    id: int
    resume_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# ----------------- Settings Schemas -----------------
class SettingBase(BaseModel):
    key: str
    value: str

class SettingCreate(SettingBase):
    """Used to create/update a setting."""
    pass

class Setting(SettingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
