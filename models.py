from sqlalchemy import Column, Integer, String
from base import Base


class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    platform = Column(String)
    quantity = Column(Integer)
