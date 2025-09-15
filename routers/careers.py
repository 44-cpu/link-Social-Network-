from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud
from database import get_db
from aws_utils import upload_file

router = APIRouter(tags=["Careers"], prefix="/careers")

# ✅ Create Career (Job Application)
@router.post("/", response_model=schemas.Career, status_code=status.HTTP_201_CREATED)
async def create_career(
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    resume: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    resume_url = None
    if resume:
        try:
            # Upload resume to AWS S3
            resume_url = upload_file(resume.file, resume.filename)
        except Exception:
            raise HTTPException(status_code=500, detail="Resume upload failed")

    career_data = schemas.CareerCreate(
        name=name,
        email=email,
        position=position,
    )

    new_career = await crud.create_career(db, career_data, resume_url)
    if not new_career:
        raise HTTPException(status_code=400, detail="Career could not be created")

    return new_career


# ✅ Get All Careers
@router.get("/", response_model=list[schemas.Career], status_code=status.HTTP_200_OK)
async def get_careers(db: AsyncSession = Depends(get_db)):
    careers = await crud.get_careers(db)
    return careers


# ✅ Get Single Career
@router.get("/{career_id}", response_model=schemas.Career, status_code=status.HTTP_200_OK)
async def get_career(career_id: int, db: AsyncSession = Depends(get_db)):
    career = await crud.get_career(db, career_id)
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    return career
