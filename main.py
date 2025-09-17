from fastapi import FastAPI
from database import engine, Base
from routers import blogs, careers
from aws_utils import init_s3 as init_career_s3
from s3_utils import init_blogs_s3  # Blogs S3 initialization 

app = FastAPI()

@app.on_event("startup")
async def startup():
    #  Create DB tables if not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Initialize Career Page S3 bucket
    init_career_s3()
    print(" Career Page S3 initialized successfully!")

    # Initialize Blogs S3 bucket
    init_blogs_s3()
    print(" Blogs S3 initialized successfully!")

# ---------------- Routers ----------------
app.include_router(blogs.router)
app.include_router(careers.router)

@app.get("/")
async def root():
    return {"status": "app running "}
