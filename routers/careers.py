# routers/careers.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud, models
from database import get_db
from aws_utils import upload_fileobj as career_upload, generate_presigned_url as career_presigned
from auth_utils import get_current_user

router = APIRouter(tags=["Careers"], prefix="/careers")

# CREATE INTERNAL JOB
@router.post("/internal", response_model=schemas.CareerOut, status_code=status.HTTP_201_CREATED)
async def create_internal_career(
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    resume: UploadFile | None = File(None),
    skills: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    resume_key = career_upload(resume.file, resume.filename) if resume else None
    career_data = schemas.CareerCreate(name=name, email=email, position=position, type="internal", resume_url=resume_key, skills=skills, user_id=current_user.id)
    new_career = await crud.create_career(db, career_data, resume_key)
    if new_career.resume_url:
        new_career.resume_url = career_presigned(new_career.resume_url)
    return new_career

# SUBMIT TO CV BANK
@router.post("/cv_bank", response_model=schemas.CareerOut, status_code=status.HTTP_201_CREATED)
async def submit_cv_bank(
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    resume: UploadFile | None = File(None),
    skills: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    resume_key = career_upload(resume.file, resume.filename) if resume else None
    career_data = schemas.CareerCreate(name=name, email=email, position=position, type="cv_bank", resume_url=resume_key, skills=skills, user_id=current_user.id)
    new_career = await crud.create_career(db, career_data, resume_key)
    if new_career.resume_url:
        new_career.resume_url = career_presigned(new_career.resume_url)
    return new_career

# GET CV BANK
@router.get("/cv_bank", response_model=list[schemas.CareerOut])
async def get_cv_bank(skill: str | None = Query(None), position: str | None = Query(None), db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    careers = await crud.get_careers(db, type="cv_bank", skill=skill, position=position)
    for c in careers:
        if c.resume_url:
            c.resume_url = career_presigned(c.resume_url)
    return careers

# GET ALL CAREERS
@router.get("/", response_model=list[schemas.CareerOut])
async def get_careers(type: str | None = None, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    careers = await crud.get_careers(db, type)
    for c in careers:
        if c.resume_url:
            c.resume_url = career_presigned(c.resume_url)
    return careers

# GET SINGLE CAREER
@router.get("/{career_id}", response_model=schemas.CareerOut)
async def get_career(career_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    career = await crud.get_career_by_id(db, career_id)
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    if career.resume_url:
        career.resume_url = career_presigned(career.resume_url)
    return career

# UPDATE CAREER
@router.put("/{career_id}", response_model=schemas.CareerOut)
async def update_career(
    career_id: int,
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    resume: UploadFile | None = File(None),
    skills: str | None = Form(None),
    type: str | None = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    career = await crud.get_career_by_id(db, career_id)
    if career.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    resume_key = career_upload(resume.file, resume.filename) if resume else None
    update_data = schemas.CareerCreate(name=name, email=email, position=position, type=type or career.type, resume_url=resume_key, skills=skills, user_id=current_user.id)
    updated_career = await crud.update_career(db, career_id, update_data)
    if updated_career.resume_url:
        updated_career.resume_url = career_presigned(updated_career.resume_url)
    return updated_career

# DELETE CAREER
@router.delete("/{career_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_career(career_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    career = await crud.get_career_by_id(db, career_id)
    if career.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    await crud.delete_career(db, career_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
