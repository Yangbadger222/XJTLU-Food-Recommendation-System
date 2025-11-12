"""FastAPI main application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.config import get_settings
from app.api import recommend_router, user_router, chat_router
from app.database import get_user_db


# Create FastAPI app
app = FastAPI(
    title="XJTLU Food Recommendation API",
    description="AI-powered food recommendation system for XJTLU students",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    settings = get_settings()
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    
    # Initialize databases
    user_db = await get_user_db()
    print("✅ Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    print("👋 Shutting down...")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommend_router)
app.include_router(user_router)
app.include_router(chat_router)

# Mount static files
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/")
async def root():
    """Root endpoint - serve the frontend."""
    static_file = Path(__file__).parent.parent / "static" / "index.html"
    if static_file.exists():
        return FileResponse(static_file)
    return {
        "message": "🍜 XJTLU Food Recommendation API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "frontend": "Frontend not found. Please check static/index.html"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }

