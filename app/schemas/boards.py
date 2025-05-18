from pydantic import BaseModel

class BoardBase(BaseModel):
    name: str
    created_by_user_id: int

class BoardCreate(BoardBase):
    pass

class Board(BoardBase):
    board_id: int

    class Config:
        from_attributes = True