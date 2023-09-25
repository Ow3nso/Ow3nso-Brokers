from apis.authentication.database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(1000))
    lastname = Column(String(1000))
    email = Column(String(1000), unique=True)
    id_number = Column(Integer, unique=True)
    country = Column(String(1000))
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User {self.email}"