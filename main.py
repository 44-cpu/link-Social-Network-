# main.py
from fastapi import FastAPI, Depends
from database import engine, Base
from routers import blogs, careers, auth, users
from aws_utils import init_s3 as init_career_s3
from s3_utils import init_blogs_s3
from auth_utils import get_current_user  # ✅ import your dependency

# ✅ Define OpenAPI security scheme (for Swagger lock icons)
openapi_security = {
    "components": {
        "securitySchemes": {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "tokenUrl": "/auth/login",
                        "scopes": {}
                    }
                },
            }
        }
    },
    "security": [{"OAuth2PasswordBearer": []}],
}

# ✅ Create FastAPI app WITHOUT global dependency
app = FastAPI(
    title="Blogs & Careers API",
    version="1.0",
    openapi_extra=openapi_security
)

# ==========================================================
# ⬇️ PUBLIC ROUTERS (no auth required)
# ==========================================================
app.include_router(auth.router)  # login/register are public
app.add_api_route("/", lambda: {"status": "App running successfully 🚀"}, tags=["Health Check"])

# ==========================================================
# ⬇️ PROTECTED ROUTERS (require valid token)
# ==========================================================
# Apply get_current_user dependency to all routes in these routers
app.include_router(users.router, dependencies=[Depends(get_current_user)])
app.include_router(blogs.router, dependencies=[Depends(get_current_user)])
app.include_router(careers.router, dependencies=[Depends(get_current_user)])

# ==========================================================
# Startup events
# ==========================================================
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    init_career_s3()
    init_blogs_s3()
