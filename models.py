from sqlalchemy import Column, Integer, String, Text
from database import Base

class Blog(Base):
    __tablename__ = "blogs" 

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500), nullable=True)  # S3 image ka link yahan save hoga
