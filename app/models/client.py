from sqlalchemy import Column, Integer, String
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
