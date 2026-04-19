from pydantic import BaseModel

class DisciplineOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class ChoiceCreate(BaseModel):
    group_id: int
    discipline_id_1: int
    discipline_id_2: int
    is_own_department_1: bool
    is_own_department_2: bool


class ChoiceOut(BaseModel):
    id: int
    group_id: int
    discipline_id_1: int
    discipline_id_2: int
    is_own_department_1: bool
    is_own_department_2: bool

    model_config = {"from_attributes": True}