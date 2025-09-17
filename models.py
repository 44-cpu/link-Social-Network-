from sqlalchemy import Column, Integer, String, Text
from database import Base

# ----------------- Blog Model -----------------
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)  # S3 image link

# ----------------- Career Model -----------------
class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    resume_url = Column(String(500), nullable=True)  # S3 resume link
    type = Column(String(50), nullable=False, default="external")  # internal/external flag

# ----------------- Settings Model -----------------
class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value = Column(String(255), nullable=False)
