import bcrypt
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserAuth(UserBase):
    password: str

    def hashed_password(self) -> bytes:
        bytePwd = self.password.encode('utf-8')

        # Hash password with salt
        return bcrypt.hashpw(bytePwd, bcrypt.gensalt())


class User(UserBase):
    profile_image_url: str

    class Config:
        orm_mode = True
