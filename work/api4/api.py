from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
from schemas import DisciplineOut, ChoiceCreate, ChoiceOut

router = APIRouter(prefix="/api")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/groups/{group_id}/disciplines", response_model=list[DisciplineOut])
def get_disciplines(group_id: int, db: Session = Depends(get_db)):
    return crud.get_available_disciplines(db, group_id)


@router.post("/choices", response_model=ChoiceOut)
def create_choice(choice: ChoiceCreate, db: Session = Depends(get_db)):
    return crud.save_choice(db, choice)

@router.get("/choices", response_model=list[ChoiceOut])
def get_choices(db: Session = Depends(get_db)):
    return crud.get_all_choices(db)