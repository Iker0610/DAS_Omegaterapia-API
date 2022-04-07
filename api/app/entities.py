from sqlalchemy import Column, String, VARCHAR, LargeBinary

from .database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(VARCHAR(length=20), name="username", primary_key=True, index=True)
    hashed_password = Column(LargeBinary, name='password')
    profile_image_url = Column(String, name='profile_image', default="/omegaterapia_api/images/account_circle.svg")
