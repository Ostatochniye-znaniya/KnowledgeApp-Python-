from database import SessionLocal
import models

db = SessionLocal()

# Очистка (опционально)
db.query(models.CheckDiscipline).delete()
db.query(models.GroupDiscipline).delete()
db.query(models.Check).delete()
db.query(models.Discipline).delete()
db.query(models.Group).delete()
db.commit()

# Группа
g = models.Group(name="ИС-21")
db.add(g)
db.commit()

# Дисциплины
d1 = models.Discipline(name="Математика")
d2 = models.Discipline(name="Программирование")
db.add_all([d1, d2])
db.commit()

# Проверка (активная)
chk = models.Check(status="Active")
db.add(chk)
db.commit()

# Связь группа — дисциплина
db.add(models.GroupDiscipline(group_id=g.id, discipline_id=d1.id))
db.add(models.GroupDiscipline(group_id=g.id, discipline_id=d2.id))

# Связь проверка — дисциплина
db.add(models.CheckDiscipline(check_id=chk.id, discipline_id=d1.id))
db.add(models.CheckDiscipline(check_id=chk.id, discipline_id=d2.id))

db.commit()
db.close()

print("Test data inserted!")