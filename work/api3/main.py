from fastapi import FastAPI
from database import Base, engine
import models
from api import router

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API is running"}