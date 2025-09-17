from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas

# -------------------- BLOG CRUD --------------------
async def create_blog(db: AsyncSession, blog: schemas.BlogCreate):
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url if blog.image_url else None
    )
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

async def get_blogs(db: AsyncSession):
    result = await db.execute(select(models.Blog))
    return result.scalars().all()

async def get_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(models.Blog).where(models.Blog.id == blog_id))
    return result.scalar_one_or_none()

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

async def delete_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(models.Blog).where(models.Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if blog:
        await db.delete(blog)
        await db.commit()
    return blog

# -------------------- CAREER CRUD --------------------
async def create_career(db: AsyncSession, career: schemas.CareerCreate, resume_url: str | None = None):
    new_career = models.Career(
        name=career.name,
        email=career.email,
        position=career.position,
        type=career.type,         #  NEW
        resume_url=resume_url
    )
    db.add(new_career)
    await db.commit()
    await db.refresh(new_career)
    return new_career

async def get_careers(db: AsyncSession, type: str | None = None):
    query = select(models.Career)
    if type:  #  filter by internal/external
        query = query.where(models.Career.type == type)
    result = await db.execute(query)
    return result.scalars().all()

async def get_career(db: AsyncSession, career_id: int):
    result = await db.execute(select(models.Career).where(models.Career.id == career_id))
    return result.scalar_one_or_none()

async def delete_career(db: AsyncSession, career_id: int):
    result = await db.execute(select(models.Career).where(models.Career.id == career_id))
    career = result.scalar_one_or_none()
    if career:
        await db.delete(career)
        await db.commit()
    return career
