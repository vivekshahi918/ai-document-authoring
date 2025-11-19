# backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr

# Schema for the request body when creating a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for the response body when returning user info
# We never want to return the password, even the hashed one!
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True # Helps Pydantic work with ORM models like SQLAlchemy
        