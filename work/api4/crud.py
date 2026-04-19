from sqlalchemy.orm import Session
from models import Discipline, GroupDiscipline, CheckDiscipline, Check, Choice


def get_active_check(db: Session):
    return (
        db.query(Check)
        .filter(Check.status == "Active")
        .order_by(Check.check_date.desc())
        .first()
    )


def get_available_disciplines(db: Session, group_id: int):
    current_check = get_active_check(db)
    if not current_check:
        return []

    return (
        db.query(Discipline)
        .join(GroupDiscipline, Discipline.id == GroupDiscipline.discipline_id)
        .join(CheckDiscipline, Discipline.id == CheckDiscipline.discipline_id)
        .filter(
            GroupDiscipline.group_id == group_id,
            CheckDiscipline.check_id == current_check.id
        )
        .all()
    )


def save_choice(db: Session, data):
    choice = Choice(
        group_id=data.group_id,
        discipline_id_1=data.discipline_id_1,
        discipline_id_2=data.discipline_id_2,
        is_own_department_1=1 if data.is_own_department_1 else 0,
        is_own_department_2=1 if data.is_own_department_2 else 0
    )

    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice


def get_all_choices(db: Session):
    return db.query(Choice).all()
