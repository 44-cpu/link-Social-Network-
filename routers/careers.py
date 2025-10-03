# routers/careers.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud
from database import get_db
from aws_utils import upload_fileobj as career_upload, generate_presigned_url as career_presigned

router = APIRouter(tags=["Careers"], prefix="/careers")

# Create Career (internal job application)
@router.post("/internal", response_model=schemas.Career, status_code=status.HTTP_201_CREATED)
async def create_internal_career(
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    resume: UploadFile | None = File(None),
    skills: str | None = Form(None),  # comma separated tags
    db: AsyncSession = Depends(get_db),
):
    resume_key = None
    if resume:
        try:
            resume_key = career_upload(resume.file, resume.filename)
        except Exception:
            raise HTTPException(status_code=500, detail="Resume upload failed")

    career_data = schemas.CareerCreate(
        name=name,
        email=email,
        position=position,
        type="internal",
        resume_url=resume_key,
        skills=skills,
    )
    new_career = await crud.create_career(db, career_data, resume_key)
    if not new_career:
        raise HTTPException(status_code=400, detail="Career could not be created")
    # add presigned url to response
    if new_career.resume_url:
        new_career.resume_url = career_presigned(new_career.resume_url)
    return new_career


# Submit to CV Bank
@router.post("/cv_bank", response_model=schemas.Career, status_code=status.HTTP_201_CREATED)
async def submit_cv_bank(
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    resume: UploadFile | None = File(None),
    skills: str | None = Form(None),  # comma separated
    db: AsyncSession = Depends(get_db),
):
    resume_key = None
    if resume:
        try:
            resume_key = career_upload(resume.file, resume.filename)
        except Exception:
            raise HTTPException(status_code=500, detail="Resume upload failed")

    career_data = schemas.CareerCreate(
        name=name,
        email=email,
        position=position,
        type="cv_bank",
        resume_url=resume_key,
        skills=skills,
    )
    new_career = await crud.create_career(db, career_data, resume_key)
    if not new_career:
        raise HTTPException(status_code=400, detail="Career could not be created")

    if new_career.resume_url:
        new_career.resume_url = career_presigned(new_career.resume_url)
    return new_career


# Get CV Bank with filters (skill / position)
@router.get("/cv_bank", response_model=list[schemas.Career], status_code=status.HTTP_200_OK)
async def get_cv_bank(
    skill: str | None = Query(None, description="Filter by skill keyword (case-insensitive)"),
    position: str | None = Query(None, description="Filter by position"),
    db: AsyncSession = Depends(get_db),
):
    # get cv_bank entries from DB and filter by skill if provided
    careers = await crud.get_careers(db, type="cv_bank", skill=skill, position=position)
    # convert resume_key -> presigned url
    for c in careers:
        if c.resume_url:
            c.resume_url = career_presigned(c.resume_url)
    return careers


# Get All Careers (optional filter ?type=internal)
@router.get("/", response_model=list[schemas.Career], status_code=status.HTTP_200_OK)
async def get_careers(type: str | None = None, db: AsyncSession = Depends(get_db)):
    careers = await crud.get_careers(db, type)
    for c in careers:
        if c.resume_url:
            c.resume_url = career_presigned(c.resume_url)
    return careers

# Get Single Career
@router.get("/{career_id}", response_model=schemas.Career, status_code=status.HTTP_200_OK)
async def get_career(career_id: int, db: AsyncSession = Depends(get_db)):
    career = await crud.get_career(db, career_id)
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    if career.resume_url:
        career.resume_url = career_presigned(career.resume_url)
    return career

# Delete Career
@router.delete("/{career_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_career(career_id: int, db: AsyncSession = Depends(get_db)):
    deleted_career = await crud.delete_career(db, career_id)
    if not deleted_career:
        raise HTTPException(status_code=404, detail="Career not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
