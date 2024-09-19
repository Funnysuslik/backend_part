import uuid
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.user import UserLogin
from app.models.user import User
from app.models.token import RefreshToken
from app.db.connection import get_db
from app.utils.security import verify_password
from app.utils.jwt import create_access_token

router = APIRouter()

@router.post("/login")
async def login_user(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where((User.username == user_login.login) | (User.email == user_login.login))
    )
    user = result.scalars().first()
    
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    
    # Create and store refresh token
    refresh_token_value = str(uuid.uuid4())  # Generate a random refresh token
    expires_at = datetime.now(datetime.timezone.utc) + timedelta(days=7)  # Refresh token expires in 7 days
    
    refresh_token = RefreshToken(
        token=refresh_token_value,
        user_id=user.id,
        expires_at=expires_at
    )
    
    db.add(refresh_token)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_value,
        "token_type": "bearer"
    }
    
@router.post("/refresh")
async def refresh_access_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    # Check if the refresh token exists and is valid
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token))
    stored_token = result.scalars().first()

    if not stored_token or stored_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    
    # Fetch the user associated with the token
    result = await db.execute(select(User).where(User.id == stored_token.user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Invalidate the old refresh token by deleting it
    await db.delete(stored_token)
    await db.commit()

    # Generate a new access token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    
    # Generate a new refresh token
    new_refresh_token_value = str(uuid.uuid4())
    new_refresh_token = RefreshToken(
        token=new_refresh_token_value,
        user_id=user.id,
        expires_at=datetime.now(datetime.timezone.utc) + timedelta(days=7)
    )
    
    db.add(new_refresh_token)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token_value,
        "token_type": "bearer"
    }