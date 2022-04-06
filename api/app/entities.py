from sqlalchemy import Column, String, VARCHAR

from .database import Base


class User(Base):
    __tablename__ = "Users"

    username = Column(VARCHAR(length=20), name="UserName", primary_key=True, index=True)
    hashed_password = Column(String, name='Password')
    profile_image_url = Column(String, name='ProfileImage', default="")  # TODO ad a default image
