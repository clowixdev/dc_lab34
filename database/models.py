from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    psw_hash = Column(String)
    pred_count = Column(Integer)
    is_admin = Column(Integer)