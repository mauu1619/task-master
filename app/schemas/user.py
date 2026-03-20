from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str


class UserShow(BaseModel):
    username: str
    email: EmailStr | None = None