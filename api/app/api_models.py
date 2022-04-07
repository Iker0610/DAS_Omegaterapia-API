from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserAuth(UserBase):
    hashed_password: str


class User(UserBase):
    profile_image_url: str

    class Config:
        orm_mode = True
