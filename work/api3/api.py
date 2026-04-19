from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from schemas import DisciplineOut

router = APIRouter(prefix="/api/groups")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{group_id}/disciplines", response_model=list[DisciplineOut])
def get_group_disciplines(group_id: int, db: Session = Depends(get_db)):
    result = crud.get_available_disciplines(db, group_id)
    if result is None:
        return []
    return result