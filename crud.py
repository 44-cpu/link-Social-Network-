# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_
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
        type=career.type,
        resume_url=resume_url or career.resume_url,
        skills=career.skills
    )
    db.add(new_career)
    await db.commit()
    await db.refresh(new_career)
    return new_career

async def get_careers(db: AsyncSession, type: str | None = None, skill: str | None = None, position: str | None = None):
    query = select(models.Career)
    filters = []
    if type:
        filters.append(models.Career.type == type)
    if skill:
        # case-insensitive match within skills string
        filters.append(models.Career.skills.ilike(f"%{skill}%"))
    if position:
        filters.append(models.Career.position.ilike(f"%{position}%"))
    if filters:
        query = query.where(and_(*filters))
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
