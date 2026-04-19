from pydantic import BaseModel

class DisciplineOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
