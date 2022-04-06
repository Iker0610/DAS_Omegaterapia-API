from sqlalchemy import Column, String, VARCHAR

from .database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(VARCHAR(length=20), name="username", primary_key=True, index=True)
    hashed_password = Column(String, name='password')
    profile_image_url = Column(String, name='profile_image', default="")  # TODO ad a default image
