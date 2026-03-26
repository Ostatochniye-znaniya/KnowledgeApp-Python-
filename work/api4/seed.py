from database import SessionLocal
import models

db = SessionLocal()

# очистка
db.query(models.CheckDiscipline).delete()
db.query(models.GroupDiscipline).delete()
db.query(models.Check).delete()
db.query(models.Discipline).delete()
db.query(models.Group).delete()
db.commit()

# группа
g = models.Group(name="ИС-21")
db.add(g)
db.commit()

# дисциплины
d1 = models.Discipline(name="Математика")
d2 = models.Discipline(name="Программирование")
db.add_all([d1, d2])
db.commit()

# активная проверка
chk = models.Check(status="Active")
db.add(chk)
db.commit()

# связи
db.add(models.GroupDiscipline(group_id=g.id, discipline_id=d1.id))
db.add(models.GroupDiscipline(group_id=g.id, discipline_id=d2.id))

db.add(models.CheckDiscipline(check_id=chk.id, discipline_id=d1.id))
db.add(models.CheckDiscipline(check_id=chk.id, discipline_id=d2.id))
db.commit()

print("Тестовые данные добавлены!")
