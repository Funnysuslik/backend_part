from pydantic import BaseModel, EmailStr, model_validator, ValidationError


# Base User schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

# User registration schema (requires password)
class UserCreate(UserBase):
    password: str
    confirm_password: str

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        return values

# User response schema (what will be sent back to the client)
class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True  # Enables ORM support for SQLAlchemy models

# User login schema
class UserLogin(BaseModel):
    login: str
    password: str
