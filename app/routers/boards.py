from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,oauth2
from ..schemas.boards import Board, BoardCreate  

router = APIRouter(
    prefix="/boards",
    tags=["Boards"]
)

@router.get("/", response_model=list[Board])
def get_boards(db: Session = Depends(get_db)):
    boards = db.query(models.Board).all()
    return boards

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Board)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    new_board = models.Board(**board.dict())
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board

@router.get("/{board_id}", response_model=Board)
def get_board(board_id: int, db: Session = Depends(get_db)):
    board = db.query(models.Board).filter(models.Board.board_id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

@router.post("/{board_id}/members", status_code=status.HTTP_201_CREATED)
def invite_member(
    board_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Check if board exists and user has permission
    board = db.query(models.Board).filter(models.Board.board_id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    if board.created_by_user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to invite members")

    # Create board member
    board_member = models.BoardMember(board_id=board_id, user_id=user_id)
    db.add(board_member)
    db.commit()
    return {"message": "Member invited successfully"}