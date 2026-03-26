
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import SessionLocal, engine
from models import Base, Group

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модель входящих данных

class GroupStatus(BaseModel):
    id: int
    status: str

@app.post("/update-status")
def update_group_status(data: List[GroupStatus], db: Session = Depends(get_db)):

    for item in data:
        group = db.query(Group).filter(Group.id == item.id).first()

        if group:
            group.status = item.status
        else:
            new_group = Group(id=item.id, status=item.status)
            db.add(new_group)

    db.commit()
    return {"message": "Statuses updated successfully"}

@app.get("/groups")
def get_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()