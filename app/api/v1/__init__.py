from fastapi import APIRouter

from .routes import auth, users


# Create a central API router
api_router = APIRouter()

# Include the auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Include the user routes
api_router.include_router(users.router, prefix="/users", tags=["users"])