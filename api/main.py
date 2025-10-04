from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.config import settings
from api.routers.auth import router as auth_router
from api.routers.companies import router as companies_router
from api.routers.users import router as users_router
from api.routers.expenses import router as expenses_router

app = FastAPI(title=settings.PROJECT_NAME)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FIX: Explicitly set prefix to "/api" to match the frontend requests (e.g., /api/auth/login)
app.include_router(auth_router, prefix="/api")
app.include_router(companies_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(expenses_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "ExesMan API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)