from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Board(Base):
    __tablename__ = 'Boards'
    
    board_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    
    creator = relationship("User", back_populates="boards")
    members = relationship("BoardMember", back_populates="board")
    columns = relationship("Column", back_populates="board")
    
class BoardMember(Base):
    __tablename__ = 'BoardMembers'
    
    board_member_id = Column(Integer, primary_key=True)
    board_id = Column(Integer, ForeignKey('Boards.board_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    
    board = relationship("Board", back_populates="members")
    user = relationship("User", back_populates="board_memberships")
    
class Column(Base):
    __tablename__ = "Columns"

    column_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    board_id = Column(Integer, ForeignKey('Boards.board_id', ondelete='CASCADE'))
    position = Column(Integer, nullable=False)
    
    board = relationship("Board", back_populates="columns")
    tasks = relationship("Task", back_populates="column")