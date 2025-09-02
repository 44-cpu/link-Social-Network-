from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas
from s3_utils import get_file_url   # 👈 helper import kiya

# Create
async def create_blog(db: AsyncSession, blog: schemas.BlogCreate):
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url if blog.image_url else None  # 👈 S3 ka URL save karega
    )
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

# Read all
async def get_blogs(db: AsyncSession):
    result = await db.execute(select(models.Blog))
    return result.scalars().all()

# Read one
async def get_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(models.Blog).where(models.Blog.id == blog_id))
    return result.scalar_one_or_none()

# Update
async def update_blog(db: AsyncSession, blog_id: int, updated_blog: schemas.BlogCreate):
    result = await db.execute(select(models.Blog).where(models.Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if blog:
        blog.title = updated_blog.title
        blog.content = updated_blog.content
        blog.image_url = updated_blog.image_url if updated_blog.image_url else blog.image_url
        await db.commit()
        await db.refresh(blog)
    return blog

# Delete
async def delete_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(models.Blog).where(models.Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if blog:
        await db.delete(blog)
        await db.commit()
    return blog
