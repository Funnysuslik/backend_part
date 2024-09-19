from fastapi import FastAPI

from .api.v1 import api_router


# Create FastAPI instance
app = FastAPI()

# Register API routes
app.include_router(api_router, prefix="/api/v1")
