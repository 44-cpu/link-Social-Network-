from fastapi import FastAPI
from database import engine, Base
from routers import router

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# include router
app.include_router(router)

@app.get("/")
async def root():
    return {"status": "ok"}
