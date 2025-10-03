# routers/blogs.py
from fastapi import APIRouter, Depends, HTTPException, Response, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud
from database import get_db
from s3_utils import upload_fileobj as upload_blog_fileobj, generate_presigned_url as blog_presigned

router = APIRouter(tags=["Blogs"], prefix="/blogs")


# Create Blog (accepts optional image upload)
@router.post("/", response_model=schemas.Blog, status_code=status.HTTP_201_CREATED)
async def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
):
    image_key = None
    if image:
        try:
            # upload and get key
            image_key = upload_blog_fileobj(image.file, key=None)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {e}")

    blog_in = schemas.BlogCreate(title=title, content=content, image_url=image_key)
    new_blog = await crud.create_blog(db, blog_in)
    if not new_blog:
        raise HTTPException(status_code=400, detail="Blog could not be created")

    # convert image_key to presigned url for response
    if new_blog.image_url:
        new_blog.image_url = blog_presigned(new_blog.image_url)

    return new_blog


# Get All Blogs
@router.get("/", response_model=list[schemas.Blog], status_code=status.HTTP_200_OK)
async def get_blogs(db: AsyncSession = Depends(get_db)):
    blogs = await crud.get_blogs(db)
    # convert keys to presigned urls
    for b in blogs:
        if b.image_url:
            b.image_url = blog_presigned(b.image_url)
    return blogs


#  Get Single Blog
@router.get("/{blog_id}", response_model=schemas.Blog, status_code=status.HTTP_200_OK)
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.image_url:
        blog.image_url = blog_presigned(blog.image_url)
    return blog


# Update Blog (optionally replace image)
@router.put("/{blog_id}", response_model=schemas.Blog, status_code=status.HTTP_200_OK)
async def update_blog(
    blog_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile | None = File(None),
    db: AsyncSession = Depends(get_db),
):
    image_key = None
    if image:
        try:
            image_key = upload_blog_fileobj(image.file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {e}")

    updated = schemas.BlogCreate(title=title, content=content, image_url=image_key)
    blog = await crud.update_blog(db, blog_id, updated)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.image_url:
        blog.image_url = blog_presigned(blog.image_url)
    return blog


# Delete Blog
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    deleted_blog = await crud.delete_blog(db, blog_id)
    if not deleted_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
