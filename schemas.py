from pydantic import BaseModel, EmailStr
from typing import Optional

# ===============================
# 🔹 USER SCHEMAS
# ===============================

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# ===============================
# 🔹 TOKEN SCHEMAS
# ===============================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# ===============================
# 🔹 BLOG SCHEMAS
# ===============================

class BlogBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None  # ✅ Added for image support

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int

    class Config:
        from_attributes = True

# ===============================
# 🔹 CAREER SCHEMAS
# ===============================

class CareerBase(BaseModel):
    name: str
    email: EmailStr
    position: str
    skills: Optional[str] = None
    type: str
    resume_url: Optional[str] = None

class CareerCreate(CareerBase):
    pass

class CareerOut(CareerBase):
    id: int

    class Config:
        from_attributes = True

# ===============================
# 🔹 SETTINGS SCHEMAS
# ===============================

class SettingBase(BaseModel):
    site_name: str
    site_description: Optional[str] = None
    contact_email: Optional[str] = None

class SettingCreate(SettingBase):
    pass

class Setting(SettingBase):
    id: int

    class Config:
        from_attributes = True
