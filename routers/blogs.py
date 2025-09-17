from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud
from database import get_db
from s3_utils import s3_client, BUCKET_NAME

router = APIRouter(tags=["Blogs"], prefix="/blogs")


# Create Blog
@router.post("/", response_model=schemas.Blog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: schemas.BlogCreate, db: AsyncSession = Depends(get_db)):
    new_blog = await crud.create_blog(db, blog)
    if not new_blog:
        raise HTTPException(status_code=400, detail="Blog could not be created")
    return new_blog


# Get All Blogs
@router.get("/", response_model=list[schemas.Blog], status_code=status.HTTP_200_OK)
async def get_blogs(db: AsyncSession = Depends(get_db)):
    blogs = await crud.get_blogs(db)
    return blogs


#  Get Single Blog
@router.get("/{blog_id}", response_model=schemas.Blog, status_code=status.HTTP_200_OK)
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


# Update Blog
@router.put("/{blog_id}", response_model=schemas.Blog, status_code=status.HTTP_200_OK)
async def update_blog(blog_id: int, updated_blog: schemas.BlogCreate, db: AsyncSession = Depends(get_db)):
    blog = await crud.update_blog(db, blog_id, updated_blog)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


# Delete Blog
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    deleted_blog = await crud.delete_blog(db, blog_id)
    if not deleted_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Get Blog Image
@router.get("/{blog_id}/image", status_code=status.HTTP_200_OK)
async def get_blog_image(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, blog_id)
    if not blog or not blog.image_url:
        raise HTTPException(status_code=404, detail="Image not found")

    key = blog.image_url.split("/")[-1]
    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
    content = obj["Body"].read()
    return Response(content, media_type="image/jpeg")
