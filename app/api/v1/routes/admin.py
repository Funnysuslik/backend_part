from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.dependencies import get_current_admin


router = APIRouter()

@router.get("/admin/dashboard")
async def get_admin_dashboard(current_user: dict = Depends(get_current_admin)):
    return {"message": f"Welcome to the admin dashboard, {current_user['sub']}"}
