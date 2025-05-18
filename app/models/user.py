from sqlalchemy import Column,Integer,String, Text
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = 'Users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    
    boards = relationship("Board", back_populates="creator")
    board_memberships = relationship("BoardMember", back_populates="user")
    task_memberships = relationship("TaskMember", back_populates="user")
