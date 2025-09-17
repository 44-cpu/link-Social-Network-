from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas, crud

router = APIRouter(tags=["Settings"], prefix="/settings")

# Create/Update Setting
@router.post("/", response_model=schemas.Setting)
async def upsert_setting(setting: schemas.SettingCreate, db: AsyncSession = Depends(get_db)):
    return await crud.upsert_setting(db, setting)
