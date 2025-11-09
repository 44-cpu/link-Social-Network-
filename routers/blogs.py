# routers/blogs.py
from fastapi import APIRouter, Depends, HTTPException, Response, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud, models
from database import get_db
from s3_utils import upload_fileobj as upload_blog_fileobj, generate_presigned_url as blog_presigned
from auth_utils import get_current_user

router = APIRouter(tags=["Blogs"], prefix="/blogs")

# CREATE BLOG
@router.post("/", response_model=schemas.BlogOut, status_code=status.HTTP_201_CREATED)
async def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    image_key = None
    if image:
        try:
            image_key = upload_blog_fileobj(image.file, image.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {e}")

    blog_in = schemas.BlogCreate(title=title, content=content, image_url=image_key, user_id=current_user.id)
    new_blog = await crud.create_blog(db, blog_in)

    if not new_blog:
        raise HTTPException(status_code=400, detail="Blog could not be created")

    if new_blog.image_url:
        new_blog.image_url = blog_presigned(new_blog.image_url)
    return new_blog

# GET ALL BLOGS
@router.get("/", response_model=list[schemas.BlogOut])
async def get_blogs(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    blogs = await crud.get_blogs(db)
    for b in blogs:
        if b.image_url:
            b.image_url = blog_presigned(b.image_url)
    return blogs

# GET SINGLE BLOG
@router.get("/{blog_id}", response_model=schemas.BlogOut)
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    blog = await crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.image_url:
        blog.image_url = blog_presigned(blog.image_url)
    return blog

# UPDATE BLOG
@router.put("/{blog_id}", response_model=schemas.BlogOut)
async def update_blog(
    blog_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    blog = await crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this blog")

    image_key = None
    if image:
        try:
            image_key = upload_blog_fileobj(image.file, image.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {e}")

    updated_blog = await crud.update_blog(db, blog_id, schemas.BlogCreate(title=title, content=content, image_url=image_key))
    if updated_blog.image_url:
        updated_blog.image_url = blog_presigned(updated_blog.image_url)
    return updated_blog

# DELETE BLOG
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    blog = await crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this blog")

    await crud.delete_blog(db, blog_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
