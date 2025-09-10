from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud
from database import get_db
from aws_utils import upload_file  # Correct function name

router = APIRouter(tags=["Careers"], prefix="/careers")

@router.post("/", response_model=schemas.Career)
async def create_career(
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    resume: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    resume_url = None
    if resume:
        # Use the correct function from aws_utils.py
        resume_url = upload_file(resume.file, resume.filename)
    
    career_data = schemas.CareerCreate(name=name, email=email, position=position)
    return await crud.create_career(db, career_data, resume_url)

@router.get("/", response_model=list[schemas.Career])
async def get_careers(db: AsyncSession = Depends(get_db)):
    return await crud.get_careers(db)

@router.get("/{career_id}", response_model=schemas.Career)
async def get_career(career_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_career(db, career_id)
