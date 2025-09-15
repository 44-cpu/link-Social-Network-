<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, Response, status
=======
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
>>>>>>> 6c2e87f4351edda155a678643ed75a5b9f58626d
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud
from database import get_db
from s3_utils import s3_client, BUCKET_NAME

router = APIRouter(tags=["Blogs"], prefix="/blogs")

<<<<<<< HEAD
# ✅ Create Blog
@router.post("/", response_model=schemas.Blog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: schemas.BlogCreate, db: AsyncSession = Depends(get_db)):
    new_blog = await crud.create_blog(db, blog)
    if not new_blog:
        raise HTTPException(status_code=400, detail="Blog could not be created")
    return new_blog


# ✅ Get All Blogs
@router.get("/", response_model=list[schemas.Blog], status_code=status.HTTP_200_OK)
async def get_blogs(db: AsyncSession = Depends(get_db)):
    blogs = await crud.get_blogs(db)
    return blogs


# ✅ Get Single Blog
@router.get("/{blog_id}", response_model=schemas.Blog, status_code=status.HTTP_200_OK)
=======
@router.post("/")
async def create_blog(blog: schemas.BlogCreate, db: AsyncSession = Depends(get_db)):
    
    response = await crud.create_blog(db, blog)
    print("****Type of response***")
    print(type(response))
    return JSONResponse(content=response, status_code=201)

@router.get("/", status_code=200)
async def get_blogs(db: AsyncSession = Depends(get_db)):
    blogs = await crud.get_blogs(db)
    return JSONResponse(content=[blog.dict() for blog in blogs], status_code=200)

@router.get("/{blog_id}", status_code=200)
>>>>>>> 6c2e87f4351edda155a678643ed75a5b9f58626d
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return JSONResponse(content=blog.dict(), status_code=200)

<<<<<<< HEAD

# ✅ Update Blog
@router.put("/{blog_id}", response_model=schemas.Blog, status_code=status.HTTP_200_OK)
=======
@router.put("/{blog_id}", status_code=200)
>>>>>>> 6c2e87f4351edda155a678643ed75a5b9f58626d
async def update_blog(blog_id: int, updated_blog: schemas.BlogCreate, db: AsyncSession = Depends(get_db)):
    blog = await crud.update_blog(db, blog_id, updated_blog)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return JSONResponse(content=blog.dict(), status_code=200)

<<<<<<< HEAD

# ✅ Delete Blog
@router.delete("/{blog_id}", status_code=status.HTTP_200_OK)
=======
@router.delete("/{blog_id}", status_code=204)
>>>>>>> 6c2e87f4351edda155a678643ed75a5b9f58626d
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    deleted_blog = await crud.delete_blog(db, blog_id)
    if not deleted_blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return JSONResponse(content=None, status_code=204)

<<<<<<< HEAD

# ✅ Get Blog Image
@router.get("/{blog_id}/image", status_code=status.HTTP_200_OK)
=======
@router.get("/{blog_id}/image", status_code=200)
>>>>>>> 6c2e87f4351edda155a678643ed75a5b9f58626d
async def get_blog_image(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await crud.get_blog(db, blog_id)
    if not blog or not blog.image_url:
        raise HTTPException(status_code=404, detail="Image not found")

    key = blog.image_url.split("/")[-1]
    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
    content = obj["Body"].read()
    return Response(content, media_type="image/jpeg")
