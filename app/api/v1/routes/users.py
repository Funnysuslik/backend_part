from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.db.connection import get_db
from app.utils.security import hash_password
from app.api.v1.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if the username or email already exists in the database
    result = await db.execute(select(User).where((User.username == user.username) | (User.email == user.email)))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create the user model instance
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    
    # Add the new user to the session and commit
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Refresh to get the new user's ID and other fields
    
    return new_user
  
@router.get("/users/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["sub"]}
  