from sqlalchemy import Column, Integer, String
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)
    
    phone_number = Column(String, nullable=True)

    role = Column(String, nullable=False)

    provider_status = Column(String, default="not_requested")