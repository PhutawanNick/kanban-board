from sqlalchemy import Column,Integer,String,Text,ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Task(Base):
    __tablename__ = "Tasks"

    task_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    position = Column(Integer, nullable=False)
    column_id = Column(Integer, ForeignKey('Columns.column_id', ondelete='CASCADE'))
    
    column = relationship("Column", back_populates="tasks")
    members = relationship("TaskMember", back_populates="task")

class TaskMember(Base):
    __tablename__ = 'TaskMembers'
    
    task_member_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('Tasks.task_id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('Users.user_id', ondelete='CASCADE'))
    
    task = relationship("Task", back_populates="members")
    user = relationship("User", back_populates="task_memberships")