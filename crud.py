# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
import models, schemas
from auth_utils import get_password_hash

# -------------------- USER CRUD --------------------
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, user_id: int, updated_user: schemas.UserUpdate):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if updated_user.username is not None:
        user.username = updated_user.username
    if updated_user.email is not None:
        user.email = updated_user.email
    if updated_user.password is not None:
        user.password = get_password_hash(updated_user.password)
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    await db.delete(user)
    await db.commit()
    return user

# -------------------- BLOG CRUD --------------------
async def create_blog(db: AsyncSession, blog: schemas.BlogCreate):
    new_blog = models.Blog(
        title=blog.title,
        content=blog.content,
        image_url=blog.image_url,
        user_id=getattr(blog, "user_id", None)
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
    if not blog:
        return None
    blog.title = updated_blog.title
    blog.content = updated_blog.content
    blog.image_url = updated_blog.image_url or blog.image_url
    await db.commit()
    await db.refresh(blog)
    return blog

async def delete_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(models.Blog).where(models.Blog.id == blog_id))
    blog = result.scalar_one_or_none()
    if not blog:
        return None
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
        skills=career.skills,
        user_id=getattr(career, "user_id", None)
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
        filters.append(models.Career.skills.ilike(f"%{skill}%"))
    if position:
        filters.append(models.Career.position.ilike(f"%{position}%"))
    if filters:
        query = query.where(and_(*filters))
    result = await db.execute(query)
    return result.scalars().all()

async def get_career_by_id(db: AsyncSession, career_id: int):
    result = await db.execute(select(models.Career).where(models.Career.id == career_id))
    return result.scalar_one_or_none()

async def update_career(db: AsyncSession, career_id: int, updated_career: schemas.CareerCreate):
    result = await db.execute(select(models.Career).where(models.Career.id == career_id))
    career = result.scalar_one_or_none()
    if not career:
        return None
    career.name = updated_career.name
    career.email = updated_career.email
    career.position = updated_career.position
    career.type = updated_career.type or career.type
    career.skills = updated_career.skills or career.skills
    career.resume_url = updated_career.resume_url or career.resume_url
    await db.commit()
    await db.refresh(career)
    return career

async def delete_career(db: AsyncSession, career_id: int):
    result = await db.execute(select(models.Career).where(models.Career.id == career_id))
    career = result.scalar_one_or_none()
    if not career:
        return None
    await db.delete(career)
    await db.commit()
    return career
