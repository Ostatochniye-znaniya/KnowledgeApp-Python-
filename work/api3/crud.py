from sqlalchemy.orm import Session
from models import Discipline, GroupDiscipline, CheckDiscipline, Check

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
        return None

    disciplines = (
        db.query(Discipline)
        .join(GroupDiscipline, Discipline.id == GroupDiscipline.discipline_id)
        .join(CheckDiscipline, Discipline.id == CheckDiscipline.discipline_id)
        .filter(
            GroupDiscipline.group_id == group_id,
            CheckDiscipline.check_id == current_check.id
        )
        .all()
    )

    return disciplines