from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud
from database import get_db
from aws_utils import upload_file

router = APIRouter(tags=["Careers"], prefix="/careers")

# Create Career (Job Application)
@router.post("/", response_model=schemas.Career, status_code=status.HTTP_201_CREATED)
async def create_career(
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    type: str | None = Form(None),  # optional now
    resume: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    resume_url = None
    if resume:
        try:
            resume_url = upload_file(resume.file, resume.filename)
        except Exception:
            raise HTTPException(status_code=500, detail="Resume upload failed")

    # agar type user ne nahi diya to DB settings se uthao
    if not type:
        type = await crud.get_setting(db, "DEFAULT_CAREER_TYPE") or "external"

    career_data = schemas.CareerCreate(
        name=name,
        email=email,
        position=position,
        type=type,
    )

    new_career = await crud.create_career(db, career_data, resume_url)
    if not new_career:
        raise HTTPException(status_code=400, detail="Career could not be created")

    return new_career

# Get All Careers (optional filter ?type=internal)
@router.get("/", response_model=list[schemas.Career], status_code=status.HTTP_200_OK)
async def get_careers(type: str | None = None, db: AsyncSession = Depends(get_db)):
    careers = await crud.get_careers(db, type)
    return careers

# Get Single Career
@router.get("/{career_id}", response_model=schemas.Career, status_code=status.HTTP_200_OK)
async def get_career(career_id: int, db: AsyncSession = Depends(get_db)):
    career = await crud.get_career(db, career_id)
    if not career:
        raise HTTPException(status_code=404, detail="Career not found")
    return career

# Delete Career
@router.delete("/{career_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_career(career_id: int, db: AsyncSession = Depends(get_db)):
    deleted_career = await crud.delete_career(db, career_id)
    if not deleted_career:
        raise HTTPException(status_code=404, detail="Career not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
